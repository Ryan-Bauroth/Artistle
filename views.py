from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv

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
