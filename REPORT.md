# 🍽️ Kitchen Secrets

## 🚀 Project Overview

**Kitchen Secrets** is a regional recipe-sharing platform designed to **preserve and celebrate India’s rich culinary heritage**. The app enables users to upload traditional recipes, explore regional cuisines on an interactive map, and contribute to a growing corpus of food knowledge that supports AI research and cultural preservation.

---

## 🎯 Problem Statement

Many traditional Indian recipes are undocumented and at risk of being lost with time. Mainstream digital platforms often overlook rural or region-specific culinary practices. **Kitchen Secrets** bridges this gap by enabling communities to share authentic recipes in their own languages, ensuring that this precious knowledge is preserved for future generations and AI datasets.

---

## 🛠️ Features

| Feature                  | Description                                                    |
|--------------------------|----------------------------------------------------------------|
| 🧾 Recipe Upload          | Add recipes with title, ingredients, process, and media        |
| 🌐 Multilingual Support  | UI and recipe entries in various Indian languages              |
| 🗺️ Map-Based Discovery    | Explore recipes by region using interactive folium map         |
| 👥 User Profiles          | Secure login, profile pictures, points & contribution stats    |
| 🔐 Encrypted Auth         | Passwords stored securely using hashing techniques             |
| 🖼️ Media Upload           | Add images/videos for richer culinary stories                  |
| 📚 Corpus Building        | Recipes tagged for language, location, and ingredients         |
| 🏆 Leaderboard & Stats    | Recognize top contributors, gamify community participation     |
| ⚙️ Admin Dashboard        | Admin access to user management and content moderation         |

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python (with local JSON-based or optional DB backend)
- **Mapping:** `streamlit-folium`, `geopy`
- **Media Handling:** `Pillow`, Streamlit file uploader
- **Corpus Support:** `sentence-transformers`, `langdetect` (or alt. language detection)
- **Deployment:** Hugging Face Spaces / GitLab Pages / Local Server

---

## 📊 Data Structure

Each recipe includes:

- 🍛 Title
- 📃 Ingredients
- 🔧 Preparation steps
- 🌐 Language and region tags
- 📍 Optional location (lat/lon)
- 🖼️ Media (image/video)
- 👤 User info (username, profile pic, points)
- 📆 Timestamp

---

## 👥 Team Contributions

| Name               | Role                             |
|--------------------|----------------------------------|
| **Ch. Thanuja**     | Project Lead, Coordination        |
| **V. Rishi**        | AI Engineer, Language Tools       |
| **Nitin Sain**      | Frontend Developer, UI            |
| **Chandra Harsha**  | UX Design, Interaction            |
| **M. Sai Kiran**    | Data Handling, Corpus Structuring |

---

## 📈 Future Scope

- 📱 Mobile-responsive version
- 📂 Exportable recipe book (PDFs by region or language)
- 🧠 AI-based ingredient/image suggestions
- 🧑‍🍳 Video recipe walkthroughs with narration
- 📡 Community radio/audio recipe sharing for elders

---

## 📄 License

This project is licensed under the **MIT License**.  
All code and contributed content are free to use with attribution.

---

## 🙏 Acknowledgements

We thank every contributor helping **preserve India’s culinary wisdom**. Your recipes are stories, and every story deserves to be remembered.

> _“Kitchen Secrets: Preserving flavors, celebrating traditions.”_ 🇮🇳
