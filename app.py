### Spotify AI Song Recommender Project

# Requirements:
# pip install spotipy pandas scikit-learn Flask

import os
import pandas as pd
import numpy as np
from flask import Flask, request, redirect, session, render_template_string
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'Spotify Recommendation Cookie'

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

SCOPE = 'user-top-read'
CACHE = '.spotipyoauthcache'

@app.route('/')
def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                             client_secret=SPOTIPY_CLIENT_SECRET,
                             redirect_uri=SPOTIPY_REDIRECT_URI,
                             scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                             client_secret=SPOTIPY_CLIENT_SECRET,
                             redirect_uri=SPOTIPY_REDIRECT_URI,
                             scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/recommendations')

@app.route('/recommendations')
def recommend():
    token_info = session.get('token_info', {})
    sp = spotipy.Spotify(auth=token_info['access_token'])

    top_tracks = sp.current_user_top_tracks(limit=50)
    track_ids = [track['id'] for track in top_tracks['items']]
    features = sp.audio_features(track_ids)

    df = pd.DataFrame(features)
    df = df.dropna(subset=['danceability', 'energy', 'valence', 'tempo'])
    X = df[['danceability', 'energy', 'valence', 'tempo']]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    user_profile = X_scaled.mean(axis=0).reshape(1, -1)
    similarities = cosine_similarity(user_profile, X_scaled)[0]
    df['similarity'] = similarities
    recommendations = df.sort_values(by='similarity', ascending=False).head(10)

    track_names = []
    for idx in recommendations.index:
        track_info = sp.track(df.loc[idx, 'id'])
        name = track_info['name']
        artist = track_info['artists'][0]['name']
        url = track_info['external_urls']['spotify']
        track_names.append(f"<li><a href='{url}'>{name}</a> by {artist}</li>")

    html = f"""
    <h1>Recommended Songs for You</h1>
    <ul>
        {''.join(track_names)}
    </ul>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
