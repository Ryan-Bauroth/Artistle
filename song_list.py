import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_artist_songs(artist_name):
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,
                                                          CLIENT_SECRET)
    spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    songs_list = []     #creates list for all artist that include the given 'artist_name' in their names
    artist_list = []    #creates list for songs of the chosen artist


    results = spot.search(a=artist_name, type='artist')     #gets the artists from spotify

    for item in results['artists']['items']:                #Adds the artist names to the list
        artist_list.append(item['name'])                

    
    results = spot.search(a="artist:"+artist_list[0], type='track', limit=50)   #gets 50 songs from artists that include 'given artist' in their name


    for track in results['tracks']['items']:
        song_name = track['name']              #gets the name of the song
        preview_url = track['preview_url']     #gets the url of the song


        artist_check = track['artists'][0]['name']  #gets the artist of the song from song url


        if song_name and preview_url and artist_check.lower().strip()==artist_name.lower().strip():  
            songs_list.append(song_name+"-"+preview_url)    #checks if the artist of the song is the needed one and creates a list with the name+url


    return songs_list




def artist_check(artist_name):

    if len(get_artist_songs(artist_name))>=10:
        return artist_name                  #if artist has more than 10 playable songs, returns artist 
    
    elif len(get_artist_songs(artist_name))<10 and len(get_artist_songs(artist_name))>0:
        return artist_name+"&%!", len(get_artist_songs(artist_name))         #if artist has between 1 and 10 playable songs, returns a different code that will allow a pop up disclaimer warning the player about the small song amount. Returns length of song list.
    
    else:
        no_url = "Artist_has_no_url"
        return no_url                       #if artist has no playable songs, returns an error




