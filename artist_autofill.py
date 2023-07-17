import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_artists(query):
    client_credentials_manager = SpotifyClientCredentials(client_id='aa6fce7db87347c5b5d0690f32ad1dd1',
                                                          client_secret='dbe95efa14544260bf8e2e1e61a29345')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_names = []

    results = sp.search(q=query, type='artist')

    for item in results['artists']['items']:
        artist_names.append(item['name'])

    return artist_names

