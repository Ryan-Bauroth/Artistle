from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv

# abstracted variables
ARTIST_AUTOFILL_NUMBER = 5

load_dotenv()

username = os.getenv('USERNAME')
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope="user-modify-playback-state")
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()

results = spotifyObject.search("yebbas hearbreak", 1, 0, "track")

songs_dict = results['tracks']
song_items = songs_dict['items']
song = song_items[0]['preview_url']
print(results)

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template('index.html', name="tim")


@views.route("/single-player")
def single_player():
    return render_template('single-player.html', song_one=song)


@views.route("/profile")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("profile.html")


@views.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})


@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)


@views.route("/gotohome")
def go_to_home():
    return redirect(url_for("views.home"))


""" Method artist_autofill
    Searches for the top spotify artists using the query input
    @param query current user input under the "artist" input
    @return artist_names the first (ARTIST_AUTOFILL_NUMBER amount) artists in a list format
"""


def artist_autofill(query):
    artist_names = []
    results = spotifyObject.search(q=query, type='artist')
    for item in results['artists']['items']:
        artist_names.append(item['name'])
    return artist_names[:ARTIST_AUTOFILL_NUMBER]


""" Method check_user_answer
    Checks if the the user's guess is correct
    @param guessed_song, actual_song the user input, the correct answer
    @return True if correct False if otherwise
"""


def check_user_answer(guessed_song, actual_song):
    if guessed_song.lower().strip() == actual_song.lower().strip():
        return True
    else:
        return False
