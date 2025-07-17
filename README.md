# 🍲 Kitchen Secrets (Rasoi Raaz)
**Preserving India's Culinary Heritage Through Open-Source & AI**

---

## 🌟 Project Overview
**Kitchen Secrets (Rasoi Raaz)** is a community-driven open-source application built using **Streamlit** that allows users to share, explore, and preserve traditional Indian recipes.  
Our goal is to collect culturally rich culinary data in multiple formats (text, images, audio, video) to create an invaluable dataset for AI models while providing users an engaging and useful platform.

---

## 🛠 Features (MVP)
- ✅ **Multi-format Recipe Submission:** Text + Images + Audio/Video
- ✅ **Regional Categorization:** Filter recipes by Indian region
- ✅ **Browse & Explore:** Interactive UI to view all contributions
- ✅ **User Reactions & Comments:** Like, love, and comment on recipes
- ✅ **Point System:** Earn points for uploads and interactions
- ✅ **Offline-First Hint:** Handles low-connectivity gracefully
- ✅ **Multilingual UI:** English, हिंदी, తెలుగు

---

## 🧩 Why It Matters
Each recipe submission contributes to a **Corpus Collection Engine**, capturing:
- Regional food vocabulary in local languages
- Step-by-step instructions
- Image-text pairs (dish visuals)
- Audio narrations (for future speech-to-text models)

---

## 🖼 Tech Stack
- **Frontend:** Streamlit  
- **Storage:** JSON (recipes, users) + Local media storage  
- **Deployment:** Hugging Face Spaces  
- **Languages Supported:** English, Hindi, Telugu  

---

## 📂 Project Structure
kitchen_secrets/
├─ app.py                  # Main Streamlit app
├─ data/
│  ├─ recipes.json         # Stores all recipes
│  ├─ users.json           # Tracks user points
├─ media/
│  ├─ images/              # Uploaded dish images
│  ├─ audio/               # Uploaded audio files
│  ├─ video/               # Uploaded videos
├─ style.css               # Custom UI styling
├─ requirements.txt
└─ README.md


---

## ▶️ How to Run Locally
### ✅ Prerequisites
- Python 3.8+
- pip (Python package manager)

### ✅ Steps
```bash
# 1. Clone the repo
git clone https://code.swecha.org/your-team/kitchen-secrets.git
cd kitchen-secrets

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate    # (Windows: venv\Scripts\activate)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py



---

## 🌍 Deployment

Deployed on Hugging Face Spaces:
👉 Click to Open App



---

## 🎯 Future Enhancements

    AI-based Ingredient Parsing

    Automatic Regional Tag Suggestion

    Community Challenges (Gamified Growth)

    Offline Sync for low-connectivity support

    AI-driven Recipe Summarization & Translation


---

## 👨‍👩‍👧 Team

    Project Lead: Ch.Thanuja

    AI Engineer: V.Rishi

    Frontend Developer: Nitin Sain

    UX Designer: Chandra Harsha

    Data Scientist: M.Sai Kiran

---

## 📜 License

This project is open-source and licensed under the MIT License.
