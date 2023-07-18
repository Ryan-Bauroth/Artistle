import spotipy
import song_list
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials('CLIENT_ID','CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_img_link(artist_name):
    results = sp.search(q='artist:' + song_list.artist_name, type='artist')

    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        return artist['images'][0]['url']
