from urllib.parse import urlencode
from flask import Blueprint, render_template, request, make_response, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv

# abstracted variables
ARTIST_AUTOFILL_NUMBER = 5
artist_check_num = -2

load_dotenv()

scope = "user-library-read, user-read-recently-played, playlist-read-private"
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()

views = Blueprint(__name__, "views")


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
        check = artist_check(user_input)
        # print(user_input)
        # print(artist_check(user_input))
        print(get_artist_songs(user_input, "Limit" if user_input + "&%!" in check else "No Limit"))
        return check if check == "Artist_has_no_url" else get_artist_songs(user_input,
                                                                           "Limit" if user_input + "&%!" in check else "No Limit"), 202


@views.route("/callback")
def callback():
    code = request.args['code']
    return redirect(url_for('views.single_player'))


@views.route("/authorize_user")
def authorize_user():
    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    params = {'response_type': 'code', 'client_id': clientID,
              'redirect_uri': redirect_uri, 'scope': scope, }
    query_params = urlencode(params)
    return make_response(redirect(authorize_url + query_params))


def get_artist_songs(artist_name, blank_space):
    songs_list = []
    artist_list = []
    if blank_space == "Limit":
        songs_list.append("Limited Selection")
    elif blank_space == "No Limit":
        songs_list.append("")

    songs_list.append(get_img_link(artist_name))

    results = spotifyObject.search(q=artist_name, type='artist')

    for item in results['artists']['items']:
        artist_list.append(item['name'])
        if len(artist_list) > 0:
            break

    results = spotifyObject.search(q="artist:" + artist_list[0], type='track', limit=50, market="US")

    for track in results['tracks']['items']:
        song_name = track['name'].replace(",", "")
        preview_url = track['preview_url']

        artist_check = track['artists'][0]['name']

        if song_name and preview_url and artist_check.lower().strip() == artist_name.lower().strip() and not duplicateSongCheck(
                song_name, songs_list):
            songs_list.append(f"{song_name}|#&{preview_url} ")

    return songs_list


def duplicateSongCheck(song_name, songs_list):
    for song in songs_list:
        if song_name == song.split("|"):
            return True
    return False


"""
"""


def artist_check(artist_name):
    if len(get_artist_songs(artist_name, "")) >= 10:
        return artist_name  # if artist has more than 10 playable songs, returns artist

    elif 10 > len(get_artist_songs(artist_name, "")) > 2:
        return artist_name + "&%!", len(get_artist_songs(artist_name, ""))  # if artist has between 1 and 10 playable
        # songs, returns a different code that will allow a pop up disclaimer warning the player about the small song
        # amount. Returns length of song list.

    else:
        no_url = "Artist_has_no_url"
        return no_url  # if artist has no playable songs, returns an error


def get_img_link(artist_name):
    results = spotifyObject.search(q='artist:' + artist_name, type='artist')
    try:
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            return artist['images'][0]['url']
    except IndexError:
        return ""


def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }

    encoded = base64.b64encode("{}:{}".format(client_id, client_secret))
    headers = {"Content-Type": HEADER, "Authorization": "Basic {}".format(encoded)}

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))
