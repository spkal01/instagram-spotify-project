import os
import time
import logging
import signal
import sys

from instagrapi import Client
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from config import (
    ACCOUNT_USERNAME,
    ACCOUNT_PASSWORD,
    APP_CLIENT_ID,
    APP_CLIENT_SECRET,
    APP_REDIRECT_URI
)

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Spotify Setup ---
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=APP_CLIENT_ID,
    client_secret=APP_CLIENT_SECRET,
    redirect_uri=APP_REDIRECT_URI,
    scope="user-read-currently-playing",
    cache_path=".spotify_cache"
))

# --- Instagram Setup ---
SESSION_FILE = "ig_session.json"
cl = Client()

def login():
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
            logging.info("Logged in to Instagram using saved session.")
            return
        except Exception as e:
            logging.warning(f"Failed to load session: {e}")

    # Fresh login fallback
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    cl.dump_settings(SESSION_FILE)
    logging.info("Fresh login to Instagram successful. Session saved.")

# --- Track State ---
last_bio = None

def execute():
    global last_bio
    try:
        response = sp.currently_playing()
        if not response or not response.get("item"):
            logging.info("No track currently playing.")
            return

        track = response['item']['name']
        artists = " and ".join([artist['name'] for artist in response['item']['artists']])
        current_bio = f"Now playing: {track} by {artists} ♪"

        if current_bio != last_bio:
            cl.account_set_biography(current_bio)
            last_bio = current_bio
            logging.info(f"Updated Instagram bio to: {current_bio}")
        else:
            logging.info("Track hasn't changed. Skipping update.")
    except Exception as e:
        logging.error(f"Error during execute(): {e}")

# --- Graceful Shutdown Handler ---
def shutdown_handler(signum, frame):
    logging.info("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# --- Main Loop ---
if __name__ == "__main__":
    login()
    while True:
        execute()
        time.sleep(300)  # 5 minutes
