 🎭 AI Mood Predictor

An AI-powered web app that detects your mood based on text input and offers curated Spotify playlists and motivational content. Built using **Flask**, **Transformers**, and **SQLite**.

---

## 🚀 Features

- Predicts user mood using a pre-trained NLP model (`distilbert-base-uncased-emotion`)
- Displays motivational quotes or videos based on mood
- Shows relevant Spotify playlists
- Stores mood history in a local SQLite database
- Allows deletion and filtering of mood history
- Clean UI with interactive elements

---

## 🛠️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME

### 2. Create virtual environment (optional but recommended)
python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Initialize the database
python init_db.py

### 5. Run the application
python app.py

Open your browser and visit:
📍 http://127.0.0.1:5000/


📦 Dependencies
Flask
Transformers
Torch
SQLite3

To generate the requirements.txt, this command was used:
pip freeze > requirements.txt
