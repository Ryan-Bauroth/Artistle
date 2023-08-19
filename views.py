import base64
import json
from urllib.parse import urlencode
from flask import Blueprint, render_template, request, make_response, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv
import requests
from spotipy import SpotifyClientCredentials

load_dotenv()

scope = "user-library-read"
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

auth_manager = SpotifyClientCredentials(clientID, clientSecret)
spotifyObject = spotipy.Spotify(auth_manager=auth_manager)

views = Blueprint(__name__, "app")


@views.route("/")
def home():
    return render_template('index.html')


@views.route("/single-player")
def single_player():
    return render_template('single-player.html')


@views.route("/store_artist_check", methods=["POST"])
def store_artist_check():
    if request.method == 'POST':
        user_input = request.form['input']
        # print(user_input)
        # print(artist_check(user_input))
        # print(get_artist_songs(user_input, "Limit" if user_input + "&%!" in check else "No Limit", spotifyObject))
        song_list = get_artist_songs(user_input, spotifyObject)
        song_list.insert(0, "Limited Selection" if len(
            song_list) < 10 else "")
        return "Artist_has_no_url" if len(song_list) < 2 else json.dumps(song_list), 202


@views.route("/store_artist_check_custom", methods=["POST"])
def store_artist_check_custom():
    if request.method == 'POST':
        user_input = request.form['input']
        tkn = request.form['token']  # token
        rtkn = request.form['refreshToken']  # refresh token
        auth_client = clientID + ":" + clientSecret
        auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()
        try:
            sp = spotipy.Spotify(tkn)
            song_list = get_artist_songs(user_input, sp)
            song_list.insert(0, "Limited Selection" if len(song_list) < 10 else "")
            return "Artist_has_no_url" if len(song_list) < 2 else json.dumps(song_list), 202
        except:
            try:
                headers = {
                    'Authorization': auth_encode,
                }
                data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': rtkn
                }
                tkn = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers).json()
                sp = spotipy.Spotify(tkn['access_token'])
                song_list = get_artist_songs(user_input, sp)
                song_list.insert(0, "Limited Selection" if len(song_list) < 10 else "")
                return "Artist_has_no_url" + "?token=" + tkn['access_token'] + rtkn if len(
                    song_list) < 2 else json.dumps(song_list) + "?token=" + tkn['access_token'] + "&rtoken=" + rtkn, 202
            except:
                song_list = get_artist_songs(user_input, spotifyObject)
                song_list.insert(0, "Limited Selection" if len(
                    song_list) < 10 else "")
                return "Artist_has_no_url" if len(song_list) < 2 else json.dumps(song_list), 202


@views.route("/artist_suggestions", methods=["POST"])
def artist_suggestions():
    if request.method == 'POST':
        param = request.form.to_dict()
        return json.dumps(get_suggestion_artists(param["input"])), 202


@views.route("/callback")
def callback():
    code = request.args['code']
    encoded_credentials = base64.b64encode(clientID.encode() + b':' + clientSecret.encode()).decode("utf-8")
    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    tokens = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers).json()
    return redirect('/single-player' + "?token=" + tokens['access_token'] + "&rtoken=" + tokens['refresh_token'])


@views.route("/authorize_user")
def authorize_user():
    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    params = {'response_type': 'code', 'client_id': clientID,
              'redirect_uri': redirect_uri, 'scope': scope, }
    query_params = urlencode(params)
    return make_response(redirect(authorize_url + query_params))


def get_artist_songs(artist_name, spotify_object=spotifyObject):
    songs_list = [get_img_link(artist_name)]

    results = spotify_object.search(q=artist_name, type='artist')

    if len(results['artists']['items']) > 0:
        base_artist_name = results['artists']['items'][0]['name']
        base_artist_id = results['artists']['items'][0]['id']
    else:
        return []

    results = spotify_object.search(q=base_artist_name, type='track', limit=50, market="US")

    for trk in results['tracks']['items']:
        song = spotify_object.track(trk['id'])
        song_name = song['name'].replace(",", "{COMMA HERE}")
        preview_url = song['preview_url']
        artist_id = song['artists'][0]['id']

        if song_name and preview_url and base_artist_id == artist_id and not duplicateSongCheck(
                song_name, songs_list):
            songs_list.append(f"{song_name}|#&{preview_url} ")
    return songs_list


def duplicateSongCheck(song_name, songs_list):
    # run both through a clean data function (possible improvment)
    for song in songs_list:
        if song is not None and song_name == song.split("|#&"):
            return True
    return False


def get_img_link(artist_name):
    results = spotifyObject.search(q=artist_name, type='artist')
    try:
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            return artist['images'][0]['url']
    except IndexError:
        return ""


def get_suggestion_artists(artist_name):
    results = spotifyObject.search(q=artist_name, type='artist')
    artist_list = []
    for artist in results['artists']['items']:
        artist_list.append(artist['name'])
    return artist_list
