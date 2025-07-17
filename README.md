# Kitchen Secrets – Preserving Culinary Heritage

## 1. Team Information
- **Team Name**: Innovault  
- **Team Members**:  
   **Ch. Thanuja** – Project Lead  
   **V. Rishi** – AI Engineer  
   **Nitin Sain** – Frontend Developer  
   **Chandra Harsha** – UX Designer  
   **M. Sai Kiran** – Data Scientist  

---

## 2. Project Overview

**Kitchen Secrets** is a Streamlit-based open-source platform that enables users to share and preserve traditional Indian recipes, particularly those tied to festivals, families, and local cultures. Recipes are enriched with geo-coordinates, contributor details, media (image, video, audio), and metadata such as category, title, and description. The app ensures only logged-in users can contribute, ensuring traceability and community trust.

This project contributes to building a **diverse, multilingual recipe corpus** that can serve future AI, cultural, and educational purposes.

---

## 3. Key Features

-  **Secure login system** – No anonymous users  
-  **Geo-coordinates** – Automatically capture or submit contributor location  
-  **User detail tracking** – Track submissions by authenticated user  
-  **Corpus categorization** – Festival, seasonal, snack/main/sweet, etc.  
-  **Title & description** – Contextual metadata for each recipe  
-  **Media uploads** – Add images, videos, and audio  
-  **Map visualization** – View recipe locations across India  
-  **Reactions & comments** – Community interaction  
-  **Leaderboard** – Sorted by contribution count  

---

## 4. Technical Architecture

###  Frontend
- Developed in **Streamlit**
- Responsive layout with step-by-step form
- Uses **Streamlit session state** for login and interaction
- Includes dropdowns, map, media uploader, and live leaderboard

###  Backend
- User and recipe data stored in `users.json` and `recipes.json`
- Media files saved locally (or base64-encoded)
- Location fetched using IP-based lookup (`ipinfo.io`)
- All data is structured for exportable corpus use

###  AI Layer (Planned / Optional)
- Use `langdetect` or FastText to detect recipe language
- Normalize ingredients and instructions using IndicTrans2
- Semantic search using SentenceTransformers
- Future: Speech-to-text for voice inputs

---

## 5. Project Structure

```
kitchen-secrets/
├── app.py                  # Main Streamlit app
├── users.json              # Stores registered user info
├── recipes.json            # Stores submitted recipes
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── assets/
│   └── logo.png            # Logo or branding assets
├── media/
│   └── ...                 # Uploaded images, audio, video files
├── .streamlit/
│   └── config.toml         # Streamlit configuration
└── utils/
    ├── auth.py             # Login/signup functionality
    └── helpers.py          # Geo, media, leaderboard utilities
```

---

## 6. User Feedback & Improvements

### Testing Approach
- Conducted with 10+ users across Telegram & WhatsApp  
- Asked users to share 1 traditional recipe with media and context  
- Monitored engagement and completion rate  

### Feedback Summary

| Feedback | Solution |
|----------|----------|
| Wanted multiple media uploads | Enabled support for video/audio |
| Location not precise | Manual pinning planned |
| Leaderboard missing | Now implemented |
| Couldn’t comment | Comment box added with username tracking |
| Slow image loading | Added compression and size check |

---

## 7. Corpus Impact

-  300+ recipes submitted in 5 languages  
-  Location metadata collected from 18+ states  
-  Dishes include Pongal, Diwali sweets, Biryani variants, tribal dishes  
-  Used in 3 regional food awareness events  
-  Exploring regional speech corpus collection via recipes

---

## 8. Sustainability & Future Use

- Datasets will be open-sourced via Hugging Face or GitHub
- Will support export in `.json`, `.csv`, `.txt`
- Planned outreach to food bloggers & NGOs
- Possible publication as an open digital cookbook
- AI fine-tuning on collected corpus (NLP & speech models)

---

## 9. Team Contributions

| Name | Role |
|------|------|
| **Ch. Thanuja** | Project Lead, Coordination |
| **V. Rishi** | AI Engineer, Language Tools |
| **Nitin Sain** | Frontend Developer, UI |
| **Chandra Harsha** | UX Design, Interaction |
| **M. Sai Kiran** | Data Handling, Corpus Structuring |

---

##  Acknowledgement

This project is part of the **Viswam.ai Open Source Fellowship**, aimed at building inclusive and culturally rich AI datasets and applications for India’s diverse regions.
