import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_artists(query):
    client_credentials_manager = SpotifyClientCredentials(client_id='',
                                                          client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_names = []

    results = sp.search(q=query, type='artist')

    for item in results['artists']['items']:
        artist_names.append(item['name'])

    return artist_names

