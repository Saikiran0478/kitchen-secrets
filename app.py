import streamlit as st
import os
import json
import hashlib
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static, st_folium
import folium
from PIL import Image
from io import BytesIO
import base64
from sentence_transformers import SentenceTransformer, util
import fasttext
import wikipedia
import pandas as pd
import altair as alt

# --- Configuration and Initialization ---
# Set page config - ensures wide layout for better content display
st.set_page_config(page_title="Kitchen Secrets", page_icon="🍲", layout="centered", initial_sidebar_state="auto")

# --- Custom CSS for Professional Look ---
st.markdown("""
<style>
    /* General body styling */
    body {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #262730;
    }

    /* Main title styling */
    h1 {
        font-family: 'Playfair Display', serif; /* A more elegant font */
        color: #D35400; /* A slightly darker, richer orange */
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 2px solid #FFDAB9; /* Light peach border */
    }

    /* Subheader styling */
    h2 {
        color: #2E8B57; /* Sea Green for section headers */
        border-bottom: 1px solid #E0E0E0;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
        font-size: 1.8em;
    }
    
    h3 {
        color: #4A4A4A; /* Dark gray for sub-sections */
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Info/Success/Warning/Error messages */
    .stAlert {
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 0.95em;
    }
    .stAlert > div { /* Target the inner div for icon and text alignment */
        align-items: center;
    }

    /* Form styling */
    form {
        padding: 25px;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* Subtle shadow */
        margin-bottom: 30px;
    }

    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #D1D1D1;
        padding: 10px 12px;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.03);
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stTextArea>div>div>textarea:focus {
        border-color: #FF6347;
        box-shadow: 0 0 0 0.1rem rgba(255, 99, 71, 0.25);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    .stButton>button.css-1fv21ad { /* Primary button specific styling */
        background-color: #FF6347;
        color: white;
        border: 1px solid #FF6347;
    }
    .stButton>button.css-1fv21ad:hover { /* Primary button hover */
        background-color: #E65A42;
        border-color: #E65A42;
    }
    .stButton>button.css-gh2j6q { /* Secondary button specific styling */
        background-color: #F0F2F6;
        color: #262730;
        border: 1px solid #D1D1D1;
    }
    .stButton>button.css-gh2j6q:hover { /* Secondary button hover */
        background-color: #E2E4E8;
        border-color: #C1C1C1;
    }


    /* Expander styling (for recipe cards) */
    .stExpander {
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        overflow: hidden; /* Ensures rounded corners apply to content */
    }
    .stExpander div[data-baseweb="accordion"] {
        border: none !important; /* Remove internal border from expander */
    }
    .stExpander button[aria-expanded="false"] { /* Closed expander header */
        background-color: #FAFAFA;
        padding: 15px 20px;
        border-bottom: 1px solid #E0E0E0;
        font-weight: bold;
        color: #333;
    }
    .stExpander button[aria-expanded="true"] { /* Open expander header */
        background-color: #F8F8F8;
        padding: 15px 20px;
        border-bottom: 1px solid #E0E0E0;
        font-weight: bold;
        color: #D35400; /* Accent color for open expander */
    }
    .stExpander .streamlit-expanderContent {
        padding: 20px;
    }

    /* Map styling */
    .stMap {
        border-radius: 12px;
        overflow: hidden; /* For map corners */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }

    /* Altair Chart container */
    .stPlotlyChart {
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        padding: 10px;
        margin-bottom: 20px;
    }
    
    /* Horizontal divider line */
    .st-emotion-cache-12fmwpl.e1nzilvr4 { /* This class is for st.divider() */
        margin-top: 3rem;
        margin-bottom: 3rem;
    }
    
    /* Sidebar styling */
    .stSidebar {
        border-right: 1px solid #E0E0E0;
    }

</style>
""", unsafe_allow_html=True)


# File paths
USERS_FILE = 'users.json'
DATA_DIR = 'data'
MEDIA_DIR = 'media' # New directory for media files

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Initialize models (only if not already in cache/session state)
@st.cache_resource
def load_models():
    embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    lang_model = fasttext.load_model("lid.176.ftz")
    return embedder, lang_model

embedder, lang_model = load_models()

# List of Indian States for dropdown
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

# --- User Management Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4) # Added indent for readability

def signup_user(username, password, name, email, location):
    users = load_users()
    if username in users:
        return False
    users[username] = {
            "password": hash_password(password),
            "name": name,
            "email": email,
            "location": location
        }
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == hash_password(password)

# --- Recipe Data Management Functions ---
def save_submission(data):
    uid = str(uuid.uuid4())
    filepath = os.path.join(DATA_DIR, f"{uid}.json")
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    return uid

def load_all_submissions():
    items = []
    for file in os.listdir(DATA_DIR):
        if file.endswith('.json'):
            with open(os.path.join(DATA_DIR, file), 'r') as f:
                try:
                    entry = json.load(f)
                    entry['id'] = file.split('.')[0]
                    items.append(entry)
                except json.JSONDecodeError:
                    st.warning(f"Skipping malformed JSON file: {file}")
    return items

def delete_submission(entry_id):
    filepath = os.path.join(DATA_DIR, f"{entry_id}.json")
    if os.path.exists(filepath):
        # Also delete associated media files
        with open(filepath, 'r') as f:
            entry_data = json.load(f)
            if 'image_path' in entry_data and entry_data['image_path']:
                img_path = os.path.join(MEDIA_DIR, entry_data['image_path'])
                if os.path.exists(img_path):
                    os.remove(img_path)
            if 'video_path' in entry_data and entry_data['video_path']:
                vid_path = os.path.join(MEDIA_DIR, entry_data['video_path'])
                if os.path.exists(vid_path):
                    os.remove(vid_path)
            if 'audio_path' in entry_data and entry_data['audio_path']:
                aud_path = os.path.join(MEDIA_DIR, entry_data['audio_path'])
                if os.path.exists(aud_path):
                    os.remove(aud_path)
        
        os.remove(filepath)
        return True
    return False

# --- AI/NLP/Geo Functions ---
def detect_language(text):
    if not text.strip():
        return "Unknown"
    try:
        pred = lang_model.predict(text.replace("\n", " "), k=1)
        return pred[0][0].replace("__label__", "")
    except Exception:
        return "Error detecting language"

def get_wiki_summary(dish):
    try:
        return wikipedia.summary(dish, sentences=2, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple Wikipedia entries found: {', '.join(e.options[:3])}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "No Wikipedia summary found for this specific dish."
    except Exception:
        return "Could not retrieve Wikipedia summary."

def get_similar_dishes(title, all_entries):
    if not all_entries:
        return []
    
    # Filter out entries that don't have a 'title' or are the current dish
    candidate_entries = [e for e in all_entries if 'title' in e and e['title'] != title]
    if not candidate_entries:
        return []

    # Create a list of titles for embedding
    candidate_titles = [e['title'] for e in candidate_entries]

    # Handle cases where there are no valid titles to embed
    if not candidate_titles:
        return []

    embeddings = embedder.encode(candidate_titles, convert_to_tensor=True)
    query_embedding = embedder.encode(title, convert_to_tensor=True)
    
    # Ensure scores are computed correctly
    scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    
    # Pair scores with candidate entries and sort
    results = sorted(zip(scores, candidate_entries), key=lambda x: -x[0])
    
    # Return top 3 unique results (excluding the dish itself, already handled by filtering candidate_entries)
    unique_similar = []
    seen_titles = set()
    for score, entry in results:
        if entry['title'] not in seen_titles:
            unique_similar.append(entry)
            seen_titles.add(entry['title'])
        if len(unique_similar) >= 3:
            break
    return unique_similar

# --- Session State Management for Login ---
# Initialize session state variables if they don't exist
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_data = {} # Store user details here
if "show_submit_form" not in st.session_state:
    st.session_state.show_submit_form = False # To control form visibility

# --- Login / Signup UI ---
if not st.session_state.authenticated:
    st.markdown("<h1>Kitchen Secrets: Culinary Journey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Unlock a World of Authentic Flavors and Festive Recipes.</h3>", unsafe_allow_html=True)
    st.divider()

    # Use a container to visually group login/signup forms
    with st.container(border=False): # Changed to border=False as custom CSS handles border/shadow
        col_login_spacer, col_login_form, col_login_spacer2 = st.columns([1, 2, 1])
        with col_login_form:
            auth_choice = st.radio(
                "Choose an option to get started:",
                ["Login", "Sign Up"],
                key="auth_choice_main",
                horizontal=True,
                help="Select 'Login' if you have an account, or 'Sign Up' to create a new one."
            )
            st.markdown("<br>", unsafe_allow_html=True) # Add some space

            if auth_choice == "Login":
                st.markdown("<h3>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
                with st.form("Login_Form", clear_on_submit=False):
                    username_login = st.text_input("Username", key="username_login")
                    password_login = st.text_input("Password", type="password", key="password_login")
                    login_submit = st.form_submit_button("Login to Kitchen Secrets")

                    if login_submit:
                        if login_user(username_login, password_login):
                            st.session_state.authenticated = True
                            st.session_state.username = username_login
                            users_data = load_users()
                            st.session_state.user_data = users_data.get(username_login, {})
                            st.success(f"🎉 Welcome back, {st.session_state.user_data.get('name', username_login)}! Redirecting...")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password. Please check your credentials.")
            elif auth_choice == "Sign Up":
                st.markdown("<h3>✨ Create a New Account</h3>", unsafe_allow_html=True)
                with st.form("Signup_Form", clear_on_submit=True):
                    username_signup = st.text_input("Choose a Username", help="This will be your unique identifier.")
                    password_signup = st.text_input("Set a Password", type="password", help="Make it strong!")
                    name_signup = st.text_input("Your Full Name", help="How you'd like to be addressed in the community.")
                    email_signup = st.text_input("Your Email", help="For important notifications (we value your privacy).")
                    location_signup = st.text_input("Your Location (e.g., city, state)", help="Helps us understand regional food trends and connect you with local dishes.")
                    signup_submit = st.form_submit_button("Join Kitchen Secrets")

                    if signup_submit:
                        if username_signup and password_signup and name_signup and email_signup and location_signup:
                            if signup_user(username_signup, password_signup, name_signup, email_signup, location_signup):
                                st.success("✅ Account created successfully! Please **Login** using your new credentials to continue.")
                                # Optionally switch to login tab after successful signup
                                st.session_state.auth_choice_main = "Login"
                                st.rerun()
                            else:
                                st.error("🚫 Username already exists. Please choose a different one.")
                        else:
                            st.warning("⚠️ Please fill in all signup fields to create your account.")
    st.stop() # Stop execution if not authenticated

# --- Authenticated Section ---
# Ensure user_data is always available right at the start of the authenticated section
user_data = st.session_state.get("user_data", {}) 
if not user_data and st.session_state.username: # If authenticated but user_data somehow empty (edge case)
    users_data = load_users()
    user_data = users_data.get(st.session_state.username, {})
    st.session_state.user_data = user_data # Update session state

st.markdown("<h1>Kitchen Secrets: Culinary Journey</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555;'>✨ Welcome, **{user_data.get('name', st.session_state.username)}**! Share your culinary traditions with the world. ✨</p>", unsafe_allow_html=True)
st.divider() # Replaced st.markdown("---") for a cleaner line

# --- Main Navigation / Action Buttons ---
col_nav1, col_nav2 = st.columns([1,1])
with col_nav1:
    if st.button("➕ Share Your Secret Recipe!", use_container_width=True, type="primary", help="Click to open the recipe submission form."):
        st.session_state.show_submit_form = not st.session_state.get('show_submit_form', False)
with col_nav2:
    if st.button("📜 Explore Existing Recipes", use_container_width=True, type="secondary", help="Browse recipes shared by the community."):
        st.session_state.show_submit_form = False # Hide form if user wants to explore
        st.rerun()
 # Ensure sections refresh if needed

# --- Recipe Submission Form (Conditionally Displayed) ---
if st.session_state.get('show_submit_form', False):
    st.markdown("<h2>📝 Submit Your Recipe</h2>", unsafe_allow_html=True)
    st.info("💡 Fields marked with a * are required.")
    
    with st.form("submit_form", clear_on_submit=True):
        st.markdown("<h3>Recipe Core Details 🍽️</h3>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            title = st.text_input("Recipe Title *", placeholder="e.g., 'Hyderabadi Biryani', 'Misal Pav'", help="Give your delicious recipe a catchy, descriptive name.")
            category = st.selectbox("Category 📂", ["Festival", "Traditional", "Street Food", "Home Style", "Dessert", "Snack", "Beverage", "Other"], help="What kind of dish is this?")
            
        with col_r2:
            state_selected = st.selectbox(
                "State or Region of Origin 📍",
                INDIAN_STATES,
                index=INDIAN_STATES.index(user_data.get("location", "Telangana")) if user_data.get("location") in INDIAN_STATES else 23,
                help="Which Indian state/region is this dish typically from? This helps categorize and map the cuisine."
            )
            loc_input = st.text_input("Specific City/Town (Optional)", value=user_data.get("location", ""), placeholder="e.g., 'Hyderabad', 'Pune'", help="Enter a specific city or town if you want to pinpoint this recipe's origin on the map.")
            
            latitude, longitude = None, None
            if loc_input:
                try:
                    geolocator = Nominatim(user_agent="kitchen-secrets-app")
                    location = geolocator.geocode(f"{loc_input}, India") # Add India to help with accuracy
                    if location:
                        latitude = location.latitude
                        longitude = location.longitude
                        st.success(f"🗺️ Coordinates found for {loc_input}: Lat {latitude:.4f}, Lon {longitude:.4f}")
                    else:
                        st.warning(f"📍 Could not find precise coordinates for '{loc_input}'. Try a more general location (e.g., 'Mumbai') or leave this field blank.")
                except Exception as e:
                    st.error(f"❌ Error getting coordinates: {e}. Please check your input or try again later.")

        st.markdown("<h3>Ingredients & Preparation 🧑‍🍳</h3>", unsafe_allow_html=True)
        ingredients = st.text_area("Ingredients (comma-separated) *", height=100, placeholder="e.g., '2 cups basmati rice, 500g chicken, 1 onion, ginger-garlic paste'", help="List all ingredients clearly, separated by commas.")
        steps = st.text_area("Steps / Instructions *", height=250, placeholder="1. Wash rice and soak for 30 mins.\n2. Marinate chicken...\n3. Layer and cook...", help="Provide clear, step-by-step instructions for preparing the dish.")
        
        st.markdown("<h3>Add Visuals & Audio 📸 (Optional)</h3>", unsafe_allow_html=True)
        st.write("Enhance your recipe with a photo, cooking video, or even a narrated guide!")
        col_media1, col_media2, col_media3 = st.columns(3)
        with col_media1:
            image_file = st.file_uploader("Upload an Image 🖼️", type=["jpg", "jpeg", "png"], help="Show off your delicious creation! (Max 5MB recommended)")
        with col_media2:
            video_file = st.file_uploader("Upload a Video 📹", type=["mp4", "mov", "webm", "mpeg", "mpg"], help="A short clip of the cooking process or the final dish. (Max 20MB recommended)")
        with col_media3:
            audio_file = st.file_uploader("Upload an Audio 🎤", type=["mp3", "wav", "ogg", "flac", "aac", "wma", "m4a", "aiff", "alac", "mpeg", "mp2"], help="Narrate the steps, share a traditional song, or capture cooking sounds. (Max 10MB recommended)")
            
        st.divider() # Cleaner separator before submit button
        submit = st.form_submit_button("🚀 Publish My Recipe!")

        if submit:
            if not title or not ingredients or not steps:
                st.error("🚨 Title, Ingredients, and Steps are required fields. Please complete them before publishing.")
            else:
                image_path = None
                if image_file:
                    image_filename = f"{uuid.uuid4()}_{image_file.name}"
                    image_path = os.path.join(MEDIA_DIR, image_filename)
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    image_path = image_filename # Store relative path/filename

                video_path = None
                if video_file:
                    video_filename = f"{uuid.uuid4()}_{video_file.name}"
                    video_path = os.path.join(MEDIA_DIR, video_filename)
                    with open(video_path, "wb") as f:
                        f.write(video_file.getbuffer())
                    video_path = video_filename # Store relative path/filename

                audio_path = None
                if audio_file:
                    audio_filename = f"{uuid.uuid4()}_{audio_file.name}"
                    audio_path = os.path.join(MEDIA_DIR, audio_filename)
                    with open(audio_path, "wb") as f:
                        f.write(audio_file.getbuffer())
                    audio_path = audio_filename # Store relative path/filename
                
                combined_text = f"{title} {ingredients} {steps}"
                detected_language = detect_language(combined_text)
                wiki_summary = get_wiki_summary(title)

                data = {
                    "username": st.session_state.username,
                    "name": user_data.get("name", st.session_state.username),
                    "email": user_data.get("email", "N/A"),
                    "location_name": loc_input,
                    "latitude": latitude,
                    "longitude": longitude,
                    "category": category,
                    "state_origin": state_selected,
                    "title": title,
                    "ingredients": ingredients,
                    "steps": steps,
                    "language": detected_language,
                    "image_path": image_path,
                    "video_path": video_path,
                    "audio_path": audio_path,
                    "wiki_info": wiki_summary,
                    "timestamp": datetime.now().isoformat()
                }
                
                recipe_id = save_submission(data)
                st.success(f"🎉 Success! Your recipe '{title}' has been submitted! (ID: {recipe_id})")
                st.balloons() # Celebrate the submission!
                st.session_state.show_submit_form = False # Hide form after submission
                st.rerun() # Refresh to show new recipe in explore section

    st.divider() # Separator after submission form section

# --- Explore Recipes Section ---
st.markdown("<h2>📜 Explore Authentic Indian Recipes</h2>", unsafe_allow_html=True)
st.write("Dive into a rich collection of traditional and modern Indian dishes from our community.")

all_recipes = load_all_submissions()

search_query = st.text_input("🔍 Search recipes...", placeholder="Search by title, ingredients, state, or category", help="Type keywords to filter recipes.")
if search_query:
    search_term = search_query.lower()
    filtered_recipes = [
        r for r in all_recipes 
        if search_term in r.get('title', '').lower() or
        search_term in r.get('ingredients', '').lower() or
        search_term in r.get('state_origin', '').lower() or
        search_term in r.get('category', '').lower()
    ]
else:
    filtered_recipes = all_recipes

if not filtered_recipes:
    st.info("😕 No recipes found matching your search. Try a different keyword or be the first to share one!")
else:
    filtered_recipes.sort(key=lambda x: x.get('timestamp', '0'), reverse=True)

    for recipe in filtered_recipes:
        with st.expander(f"🍽️ **{recipe.get('title', 'Untitled Recipe')}** | by {recipe.get('name', recipe.get('username', 'Unknown'))} from {recipe.get('state_origin', 'Unknown State')}"):
            
            # Use columns for media and details side-by-side
            col_display_media, col_display_details = st.columns([1, 2])
            
            with col_display_media:
                st.markdown("<h6>Media 📸</h6>", unsafe_allow_html=True)
                if recipe.get("image_path"):
                    full_image_path = os.path.join(MEDIA_DIR, recipe["image_path"])
                    if os.path.exists(full_image_path):
                        try:
                            # Use a fixed width for images in expander for consistency
                            st.image(full_image_path, caption=recipe.get('title', ''), width=200) 
                        except Exception as e:
                            st.warning(f"Could not load image: {e}")
                    else:
                        st.info("Image file not found.")
                else:
                    st.text("No image uploaded.")

                if recipe.get("video_path"):
                    full_video_path = os.path.join(MEDIA_DIR, recipe["video_path"])
                    if os.path.exists(full_video_path):
                        try:
                            video_bytes = open(full_video_path, 'rb').read()
                            st.video(video_bytes)
                        except Exception as e:
                            st.warning(f"Could not load video: {e}")
                    else:
                        st.info("Video file not found.")

                if recipe.get("audio_path"):
                    full_audio_path = os.path.join(MEDIA_DIR, recipe["audio_path"])
                    if os.path.exists(full_audio_path):
                        try:
                            audio_bytes = open(full_audio_path, 'rb').read()
                            st.audio(audio_bytes)
                        except Exception as e:
                            st.warning(f"Could not load audio: {e}")
                    else:
                        st.info("Audio file not found.")
            
            with col_display_details:
                st.markdown("<h6>Recipe Overview 📝</h6>", unsafe_allow_html=True)
                st.markdown(f"**Category:** `{recipe.get('category', 'N/A')}`")
                st.markdown(f"**Origin:** {recipe.get('location_name', 'N/A')} ({recipe.get('state_origin', 'N/A')})")
                st.markdown(f"**Submitted On:** `{datetime.fromisoformat(recipe['timestamp']).strftime('%Y-%m-%d %H:%M')}`")
                
                st.markdown("---")
                st.markdown("**Ingredients:**")
                st.markdown(f"_{recipe.get('ingredients', 'N/A')}_")
                
                st.markdown("**Instructions:**")
                st.markdown(f"_{recipe.get('steps', 'N/A')}_")
                
                st.markdown("---")
                st.markdown("<h6>AI Insights 🧠</h6>", unsafe_allow_html=True)
                st.markdown(f"**Language Detected:** `{recipe.get('language', 'N/A').upper()}`")
                st.markdown(f"**Wikipedia Summary:** _{recipe.get('wiki_info', 'No specific Wikipedia information available for this dish.')}_")
                
                # Similar Dishes
                similar_dishes = get_similar_dishes(recipe.get('title', ''), all_recipes)
                if similar_dishes:
                    st.markdown("---")
                    st.markdown("<h6>👨‍🍳 You might also like:</h6>", unsafe_allow_html=True)
                    for s_dish in similar_dishes:
                        st.markdown(f"- **{s_dish.get('title', 'Unknown Dish')}** from {s_dish.get('state_origin', 'Unknown State')}")
                else:
                    st.text("No similar recipes found in our collection yet.")

                # Delete Button (only for owner)
                if recipe.get('username') == st.session_state.username:
                    st.divider()
                    if st.button(f"🗑️ Delete This Recipe: {recipe.get('title', 'Untitled')}", key=f"delete_btn_{recipe['id']}", type="secondary", help="Permanently remove this recipe from the collection."):
                        if delete_submission(recipe['id']):
                            st.success("✅ Recipe deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete recipe.")
st.divider() # Separator after explore recipes section

# --- Map of Recipes ---
st.markdown("<h2>🗺️ Culinary Map of India</h2>", unsafe_allow_html=True)
st.write("Visualize the geographical origins of our shared recipes across India.")

map_data = pd.DataFrame([
    {   
        "latitude": r['latitude'], 
        "longitude": r['longitude'], 
        "name": r.get('title', 'Recipe'), 
        "state": r.get('state_origin', 'Unknown')
    }
    for r in all_recipes 
    if r.get('latitude') is not None and r.get('longitude') is not None
])

if not map_data.empty:
    map_data['latitude'] = pd.to_numeric(map_data['latitude'])
    map_data['longitude'] = pd.to_numeric(map_data['longitude'])

    center_lat = map_data['latitude'].mean() if not map_data.empty else 20.5937
    center_lon = map_data['longitude'].mean() if not map_data.empty else 78.9629

    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    for idx, row in map_data.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']],
            tooltip=f"**{row['name']}** from {row['state']}"
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
else:
    st.info("📍 No recipes with location data available to display on the map yet. Submit a recipe with a city/town to see it here!")

# --- Recipe Statistics ---
st.divider()
st.markdown("<h2>📊 Recipe Statistics & Trends</h2>", unsafe_allow_html=True)
st.write("Gain insights into the diverse culinary data shared by our community.")

if all_recipes:
    df_stats = pd.DataFrame(all_recipes)

    # Chart 1: Recipes per State of Origin
    st.markdown("<h3>Recipes by State/Region</h3>", unsafe_allow_html=True)
    if 'state_origin' in df_stats.columns and not df_stats['state_origin'].empty:
        state_counts = df_stats['state_origin'].value_counts().reset_index()
        state_counts.columns = ['State', 'Count']
        chart_state = alt.Chart(state_counts).mark_bar().encode(
            x=alt.X('State:N', sort='-y', title='State/Region'),
            y=alt.Y('Count:Q', title='Number of Recipes'),
            tooltip=['State', 'Count'],
            color=alt.value("#FF6347") # Use primary color for bars
        ).properties(
            title='Distribution of Recipes by State/Region',
            width=650, height=400
        ).interactive() # Make chart interactive for zooming/panning
        st.altair_chart(chart_state, use_container_width=True)
    else:
        st.info("No 'State of Origin' data available for statistics yet.")

    # Chart 2: Recipes per Category
    st.markdown("<h3>Recipes by Category</h3>", unsafe_allow_html=True)
    if 'category' in df_stats.columns and not df_stats['category'].empty:
        category_counts = df_stats['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        chart_category = alt.Chart(category_counts).mark_bar().encode(
            x=alt.X('Category:N', sort='-y', title='Recipe Category'),
            y=alt.Y('Count:Q', title='Number of Recipes'),
            tooltip=['Category', 'Count'],
            color=alt.value("#2E8B57") # Use a secondary color for bars
        ).properties(
            title='Distribution of Recipes by Category',
            width=650, height=400
        ).interactive()
        st.altair_chart(chart_category, use_container_width=True)
    else:
        st.info("No 'Category' data available for statistics yet.")
else:
    st.info("No recipes submitted yet to generate statistics.")


# --- Export Option ---
st.divider()
st.markdown("<h2>📦 Data Export</h2>", unsafe_allow_html=True)
st.write("Seamlessly export all community recipe data for offline analysis or backup.")

if st.button("📥 Export All Recipes Data (JSON)", type="secondary", use_container_width=True, help="Downloads all recipe data as a JSON file."):
    if all_recipes:
        st.download_button(
            label="Download recipes_export.json",
            data=json.dumps(all_recipes, indent=4),
            file_name="recipes_export.json",
            mime="application/json"
        )
        st.success("Download initiated!")
    else:
        st.warning("No recipes to export yet!")

# --- Footer & Logout ---
st.divider()
st.markdown("<p style='text-align: center; color: #808080; font-size: 0.8em;'>👨‍🍳 Powered by Innovault | Kitchen Secrets © 2025</p>", unsafe_allow_html=True)

# Logout in Sidebar (more professional placement)
st.sidebar.markdown("---")
st.sidebar.markdown(f"Logged in as: **{user_data.get('name', st.session_state.username)}**")
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_data = {}
    st.info("You have been logged out.")
    st.rerun()
