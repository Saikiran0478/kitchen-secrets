Got it! Here's an **updated version** of your **Project Overview** that **explicitly includes the point** that the app **collects and stores all data posted by users**, including **text, images, audio, video, geo-coordinates**, and **metadata**. This is framed clearly under both **Features** and **Corpus Contribution** sections.

---

# 🍲 Kitchen Secrets - Unveiling India's Culinary Heritage (Rasoi Raaz)

---

## 📌 Project Overview

**Kitchen Secrets** (Rasoi Raaz) is a community-driven, open-source **Streamlit application** dedicated to preserving and celebrating India’s diverse family recipes. It allows users to share regional culinary knowledge via **text, images, audio, and video**, ensuring traditional recipes are archived and passed on for generations.

It also acts as a **"Corpus Collection Engine"**, capturing rich, multimodal, multilingual culinary data from everyday Indian kitchens.

---

## 👥 Team Information

* **Project Lead:** Ch. Thanuja
* **AI Engineer:** V. Rishi
* **Frontend Developer:** Nitin Sain
* **UX Designer:** Chandra Harsha
* **Data Scientist:** M. Sai Kiran

---

## 🚀 Features (MVP)

* **Multi-format Recipe Submission:** Submit recipes through:

  * Text (typed or handwritten),
  * Images (dishes, handwritten notes),
  * Audio (narrations),
  * Video (cooking walkthroughs).
* **Geo Coordinates Capture:** Automatically or manually capture location (latitude, longitude) with each submission.
* **User Details:** Collect contributor info — name, email (optional), and demographics (optional).
* **Regional Categorization:** Tag recipes based on Indian states/regions.
* **Corpus Category Selection:** Users must choose the type of corpus being contributed:

  * *Text*, *Image-Text Pair*, *Audio-Text Pair*, *Video-Text Pair*
* **File + Description Input:** All uploads include both the media file and a description (ingredients, process, context).
* **Interactive Browsing:** Filter by region, format, popularity.
* **Reactions & Comments:** Engage with likes, hearts, and comments.
* **Point System:** Earn points for uploading and interacting.
* **Offline-First Design:** Supports queuing uploads offline and syncing later.
* **Optimized Media Uploads:** Client-side compression ensures uploads are bandwidth-friendly.
* **Multilingual Interface:** UI is localized in major Indian languages.
* **Basic AI Assistance:** Suggests regional tags and extracts ingredients/instructions from text.
* **🔐 Data Collection:**
  ✅ The app **collects and stores** all data submitted by users — including **text, images, audio, video, geo-coordinates, user info, and metadata** — for the purpose of creating a **searchable, multilingual, multimodal corpus of Indian recipes**.

---

## 🧠 Corpus Contribution

Every submission enriches a growing **AI-ready corpus** that supports cultural preservation and future research. Each entry includes:

* ✅ **Media Content** (Text, Images, Audio, Video)
* ✅ **Geo Coordinates** (Latitude, Longitude)
* ✅ **User Details** (Name, optional demographic info)
* ✅ **Corpus Category** (Text, Image-Text, etc.)
* ✅ **Recipe Metadata** (Region, language/dialect, format, file type)
* ✅ **Structured Description** (Ingredients, steps, cultural context)

This data enables:

* **Cultural Archiving**: Preserving India’s culinary diversity.
* **AI Training**: Supporting future multilingual, multimodal NLP and vision models.
* **Cross-regional Insights**: Understanding food patterns, vocabularies, and regional identities.

---

## 🧰 Technical Stack

* **Frontend:** Streamlit
* **Backend & Storage:**

  * Metadata: JSON files (scalable to SQLite)
  * Media: Stored in Hugging Face Spaces filesystem (MVP)
  * Offline Queue: Browser IndexedDB/LocalStorage
* **AI/NLP:**

  * Libraries: spaCy, custom rule-based parsers
  * Media Compression: Client-side libraries (e.g., `browser-image-compression`, `ffmpeg`)
* **Deployment:** Hugging Face Spaces

---

## ⚙️ Getting Started

### ✅ Prerequisites

* Python 3.8+
* pip (Python package installer)

### 🔧 Local Development Setup

```bash
# Clone the repo
git clone https://code.swecha.org/your-team-name/kitchen-secrets.git
cd kitchen-secrets

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App opens in browser: [http://localhost:8501](http://localhost:8501)

---

Would you like me to prepare this as a `README.md` or `REPORT.md` file formatted for GitHub or Hugging Face Spaces?
