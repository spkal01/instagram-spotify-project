from instagrapi import Client
from instagrapi import AccountMixin
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=APP_CLIENT_ID,
                                               client_secret=APP_CLIENT_SECRET,
                                               redirect_uri=APP_REDIRECT_URI,
                                               scope="user-read-currently-playing"))
response = sp.currently_playing()
track = response['item']['name']
artists = " and ".join([artist['name'] for artist in response['item']['artists']])
bio = "Now playing: " + track + " by " + artists + " ♪"
cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD, True)
cl.account_set_biography(bio)