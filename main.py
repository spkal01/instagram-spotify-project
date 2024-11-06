from instagrapi import Client
from instagrapi import AccountMixin
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from config import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=APP_CLIENT_ID,
                                               client_secret=APP_CLIENT_SECRET,
                                               redirect_uri=APP_REDIRECT_URI,
                                               scope="user-read-currently-playing"))
cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD, True)
def execute():
    response = sp.currently_playing()
    if response == None:
        return
    else:
        track = response['item']['name']
        artists = " and ".join([artist['name'] for artist in response['item']['artists']])
        bio = "Now playing: " + track + " by " + artists + " ♪"
        cl.account_set_biography(bio)

while True:
    execute()
    time.sleep(300)