import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_artist_songs(artist_name):
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,
                                                          CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    songs_list = []
    artist_list = []


    results = sp.search(q=artist_name, type='artist')

    for item in results['artists']['items']:
        artist_list.append(item['name'])

    
    results = sp.search(q="artist:"+artist_list[0], type='track', limit=50)


    for track in results['tracks']['items']:
        song_name = track['name']
        preview_url = track['preview_url']


        artist_check = track['artists'][0]['name']


        if song_name and preview_url and artist_check.lower().strip()==artist_name.lower().strip():
            songs_list.append(f"{song_name}-{preview_url} ") 


    return songs_list




def artist_check(artist_name):

    if len(get_artist_songs(artist_name))>=10:
        return artist_name
    
    elif len(get_artist_songs(artist_name))<10 and len(get_artist_songs(artist_name))>0:
        return artist_name+"&%!"
    
    else:
        no_url = "Artist_has_no_url"
        return no_url




