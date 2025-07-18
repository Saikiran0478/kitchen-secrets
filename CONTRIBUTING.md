# Contributing to Kitchen Secrets

🎉 Thank you for your interest in contributing to Kitchen Secrets! This project thrives on community involvement and we’re excited to have your support.

Kitchen Secrets is an open-source, culturally-focused platform to preserve and promote traditional Indian recipes. Your contributions—whether in the form of code, recipes, design, documentation, or feedback—help us build a richer culinary and linguistic heritage.

---

## 🧠 Before You Begin

Please make sure you've read the following:

- [README.md](./README.md) – to understand project goals and structure
- [LICENSE](./LICENSE) – MIT license under which this project is released

---

## 🚀 Ways to Contribute

You can contribute to this project in multiple ways:

### 👩‍💻 Code Contributions

- Add new features (e.g., support for more languages, filters, media tools)
- Improve UI/UX for recipe submission and browsing
- Optimize login/authentication process
- Fix bugs (see Issues section)

### 📝 Recipe Submissions

- Submit traditional Indian recipes via the app with all details (category, state, description, media)
- Include historical or cultural context wherever possible
- Upload recipes in your native language – we support many Indic scripts

### 🌐 Language & AI

- Help improve Indic language detection or translation models
- Fine-tune recipe classification or semantic similarity using Hugging Face models
- Submit training data (translations, transcriptions, etc.)

### 🎨 Design

- Enhance the logo, app UI, or user flow diagrams
- Suggest better layout or mobile responsiveness improvements

### 🔧 Infrastructure

- Help with Dockerization, CI/CD, or deployment
- Integrate databases or cloud storage solutions

---

## 🛠 Development Setup

1. Clone the repository:

   git clone https://github.com/<your-org>/kitchen-secrets.git

2. Create and activate virtual environment:

   python -m venv venv  
   source venv/bin/activate  # on Windows use: venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run Streamlit:

   streamlit run app.py

---

## 🧪 Testing

- Test all UI changes on different devices
- Use dummy accounts to test login, recipe submission, and media upload
- Run linters (e.g. black, flake8) for formatting

---

## 📋 Submitting a Pull Request

1. Fork the repo and create a branch:

   git checkout -b feature/your-feature-name

2. Make your changes, commit, and push:

   git commit -m "Added feature X"  
   git push origin feature/your-feature-name

3. Open a Pull Request on the main repository

4. Fill the PR template including:
   - What you’ve changed
   - Why you made it
   - Any open questions or suggestions

---

## 🧩 Project Structure

