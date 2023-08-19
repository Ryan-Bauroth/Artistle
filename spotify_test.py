import spotipy
import json
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Consts
username = os.getenv('USERNAME')
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

auth_manager = SpotifyClientCredentials(clientID, clientSecret)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None




