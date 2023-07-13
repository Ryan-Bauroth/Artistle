import spotipy
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Consts - TODO hide these better before github
username = os.getenv('USERNAME')
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')



# Get token for server
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope="user-modify-playback-state")
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()


# Print user information (for testing)
# print(json.dumps(user_name, sort_keys=True, indent=4))

def getuserinput():
    search_song = input("Enter the song name: ")
    search_artist = input("Enter song artist: ")
    search_album = input("Enter song album: ")
    return search_album + search_song + search_artist

results = spotifyObject.search(getuserinput(), 1, 0, "track")
print(json.dumps(results, sort_keys=True, indent=4))
songs_dict = results['tracks']
song_items = songs_dict['items']
song = song_items[0]['preview_url']
print(song)


#print(json.dumps(spotifyObject.recommendation_genre_seeds(), sort_keys=True, indent=4))
