import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def search_artists(query):
    finallist = []
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,
                                                          CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_names = []

    results = sp.search(q=query, type='artist')

    for item in results['artists']['items']:
        artist_names.append(item['name'])

    finallist = artist_names[:5]
    return finallist

    




