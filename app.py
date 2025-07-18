import streamlit as st
import os
import json
from datetime import datetime
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from utils.utils import load_users, save_submission
from PIL import Image

# Set page config
st.set_page_config(page_title="Kitchen Secrets", page_icon="🍲", layout="centered")

# Load users
users = load_users()

# Session state login management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Login
if not st.session_state.authenticated:
    with st.form("Login"):
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            if username in users and users[username]["password"] == password:
                st.success(f"Welcome, {users[username]['name']}!")
                st.session_state.authenticated = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
    st.stop()

# Authenticated section
st.title("🍛 Kitchen Secrets – Share Your Festival Flavors")

user_data = users[st.session_state.username]
st.markdown(f"👤 Logged in as: `{user_data['name']}` | 📍 Location: `{user_data['location']}`")

# Recipe Submission Form
with st.form("submit_form"):
    st.header("📝 Submit a Recipe")

    title = st.text_input("📌 Recipe Title")
    category = st.selectbox("📂 Category", ["Festival", "Traditional", "Street Food", "Home Style"])
    description = st.text_area("🗒️ Description / Steps", height=150)
    language = st.selectbox("🌐 Language", ["Telugu", "Hindi", "Tamil", "Marathi", "English"])

    # Location (Geo-coordinates)
    loc_input = st.text_input("📍 Enter your location for map", value=user_data.get("location", ""))
    geo = Nominatim(user_agent="kitchen-app")
    location = geo.geocode(loc_input)

    media_file = st.file_uploader("📷 Upload an image / audio / video", type=["jpg", "jpeg", "png", "mp4", "mp3"])

    submit = st.form_submit_button("Submit")

    if submit:
        if not title or not description:
            st.warning("Title and description are required.")
        else:
            file_url = None
            if media_file:
                os.makedirs("uploads", exist_ok=True)
                file_path = os.path.join("uploads", media_file.name)
                with open(file_path, "wb") as f:
                    f.write(media_file.read())
                file_url = file_path

            data = {
                "username": st.session_state.username,
                "name": user_data["name"],
                "email": user_data["email"],
                "location_name": loc_input,
                "latitude": location.latitude if location else None,
                "longitude": location.longitude if location else None,
                "category": category,
                "title": title,
                "description": description,
                "language": language,
                "media_file": file_url,
                "timestamp": datetime.now().isoformat()
            }

            os.makedirs("data", exist_ok=True)
            save_submission(data, st.session_state.username)
            st.success("Recipe submitted successfully! ✅")

            if location:
                m = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
                folium.Marker([location.latitude, location.longitude], tooltip=title).add_to(m)
                st.markdown("### 📍 Submission Location")
                folium_static(m)

# Footer
st.markdown("---")
st.markdown("👨‍🍳 Powered by Innovault | © 2025 Kitchen Secrets")
