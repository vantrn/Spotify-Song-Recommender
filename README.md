# 🎧 Spotify AI Song Recommender

This project uses the Spotify Web API and a simple AI model to recommend songs similar to those you already love. It fetches your top tracks, analyzes their audio features, and finds others that match your musical taste using cosine similarity.

---

## 🚀 Features

- 🔐 Spotify OAuth login to access your top tracks
- 📊 Uses audio features like energy, valence, and danceability
- 🧠 AI-powered recommendations using cosine similarity
- 🌐 Flask web interface that displays song recommendations as clickable Spotify links

---

## 📦 Tech Stack

- Python
- Flask (for web interface)
- Spotipy (Spotify Web API wrapper)
- Pandas, NumPy
- Scikit-learn (for scaling and similarity calculations)

---

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/spotify-ai-recommender.git
cd spotify-ai-recommender
```

### 2. Install 
```bash
pip install -r requirements.txt
```

### 3. Register a Spotify App
Go to the Spotify Developer Dashboard and:
Click Create an App
Set Redirect URI to: http://localhost:5000/callback
Copy your Client ID and Client Secret

### 4. Configure app.py
Open app.py and replace:
```python
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
app.secret_key = 'your_secret_key'
```

### 5. Run the app
```bash
python app.py
```
and then go to your browser and go to
```arduino
http://localhost:5000
```