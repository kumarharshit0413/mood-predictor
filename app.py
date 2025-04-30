from flask import Flask, render_template, request, url_for, jsonify,redirect
import json
import sqlite3
from datetime import datetime, timedelta
from transformers import pipeline

app = Flask(__name__)

# Load a sentiment analysis pipeline
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

# Load resources from JSON
with open("resources.json", "r", encoding="utf-8") as f:
    resources = json.load(f)

# ----- DATABASE SETUP -----
def save_to_db(text, mood):
    conn = sqlite3.connect('mood.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            text TEXT NOT NULL,
            mood TEXT NOT NULL
        )
    ''')
    c.execute("INSERT INTO mood_history (timestamp, text, mood) VALUES (?, ?, ?)",
              (datetime.now().isoformat(), text, mood))
    conn.commit()
    conn.close()

# Spotify playlists based on mood
mood_spotify_map = {
    "Happy 😊": "https://open.spotify.com/embed/track/3xMHXmedL5Rvfxmiar9Ryv?utm_source=generator",
    "Sad 😢": "https://open.spotify.com/embed/track/4LMlVCXHJtCE9abhmn0mYo?utm_source=generator",
    "Angry 😠": "https://open.spotify.com/embed/track/7vZz8oJ5qAqB9MghufRK5k?utm_source=generator",
    "Fearful 😨": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
    "Disgusted 🤢": "https://open.spotify.com/embed/playlist/37i9dQZF1DWSqBruwoIXkA",
    "Surprised 😮": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0BcQWzuB7ZO",
    "Neutral 😐": "https://open.spotify.com/embed/track/7lvDsmTRXFE3dK4OjvRiWB?utm_source=generator"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"].lower()
    # Predict mood using the model
    result = classifier(text)[0]
    label = result['label'].capitalize()

    # Map model output to emojis
    mood_map = {
        "Joy": "Happy 😊",
        "Anger": "Angry 😠",
        "Sadness": "Sad 😢",
        "Fear": "Fearful 😨",
        "Disgust": "Disgusted 🤢",
        "Surprise": "Surprised 😮",
        "Neutral": "Neutral 😐"
    }
    mood = mood_map.get(label, "Neutral 😐")

    # Save to DB
    save_to_db(text, mood)

    # if any(word in text for word in [
    #     "happy", "joyful", "excited", "cheerful", "glad", "content", "satisfied",
    #     "awesome", "fantastic", "great", "good", "positive", "delighted", "overjoyed",
    #     "smiling", "grateful", "thrilled", "blessed", "joyous", "peaceful", "hopeful",
    #     "wonderful", "ecstatic", "bright", "elated", "sunny"
    # ]):
    #     mood = "Happy 😊"
    # elif any(word in text for word in [
    #     "sad", "down", "unhappy", "depressed", "low", "upset", "gloomy", "blue",
    #     "miserable", "heartbroken", "crying", "hurt", "disappointed", "lonely",
    #     "hopeless", "worthless", "broken", "sorrow", "tearful", "grieving", "drained"
    # ]):
    #     mood = "Sad 😢"
    # elif any(word in text for word in [
    #     "angry", "mad", "furious", "annoyed", "irritated", "pissed", "upset", "frustrated",
    #     "enraged", "fuming", "infuriated", "outraged", "livid", "resentful", "boiling",
    #     "exploding", "raging", "offended", "snappy", "tense", "bitter", "grumpy"
    # ]):
    #     mood = "Angry 😠"
    # elif any(word in text for word in [
    #     "scared", "afraid", "terrified", "nervous", "anxious", "worried", "fearful",
    #     "petrified", "shaky", "panicked", "frightened", "horrified", "spooked", "tense"
    # ]):
    #     mood = "Fearful 😨"
    # elif any(word in text for word in [
    #     "disgusted", "gross", "nasty", "repulsed", "sickened", "yuck", "revolted",
    #     "cringe", "dirty", "vile", "filthy", "displeased", "repelled"
    # ]):
    #     mood = "Disgusted 🤢"
    # elif any(word in text for word in [
    #     "surprised", "shocked", "amazed", "startled", "astonished", "speechless",
    #     "stunned", "whoa", "wow", "unexpected", "unbelievable", "mind-blown"
    # ]):
    #     mood = "Surprised 😮"
    # else:
    #     mood = "Neutral 😐"

    # # Save the result to the database
    # save_to_db(text, mood)

    # Load the resource
    resource = resources.get(mood)
    resource["url"] = resource["content"] if resource else None

    # Get Spotify link
    spotify_url = mood_spotify_map.get(mood, "")

    return render_template("index.html",
                           mood=mood,
                           text=text,
                           resource=resource,
                           spotify_url=spotify_url)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# DELETE ROUTE
@app.route("/delete", methods=["POST"])
def delete_history():
    conn = sqlite3.connect("mood.db")
    c = conn.cursor()
    c.execute("DELETE FROM mood_history")
    conn.commit()
    conn.close()
    return redirect("/")

# Route to fetch mood history with optional filters
@app.route("/history")
def history():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    preset = request.args.get("preset")

    conn = sqlite3.connect('mood.db')
    c = conn.cursor()

    query = "SELECT timestamp, mood FROM mood_history"
    params = []

    if preset:
        now = datetime.now()
        if preset == "last_7_days":
            start = now - timedelta(days=7)
            end = now
        elif preset == "last_30_days":
            start = now - timedelta(days=30)
            end = now
        else:
            start = end = None
    elif start_date_str and end_date_str:
        start = datetime.fromisoformat(start_date_str)
        end = datetime.fromisoformat(end_date_str)
    else:
        start = end = None

    if start and end:
        query += " WHERE timestamp BETWEEN ? AND ?"
        params.extend([start.isoformat(), end.isoformat()])

    query += " ORDER BY timestamp ASC"
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)