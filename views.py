from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv
import random

# abstracted variables
ARTIST_AUTOFILL_NUMBER = 5
artist_check_num = -2

load_dotenv()

clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope="user-modify-playback-state")
token_dict = oauth_object.get_access_token()
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
        artist_name = request.form['input']
        check = artist_check(artist_name)
        print(artist_name)
        print(artist_check(artist_name))
        print(get_artist_songs(artist_name, "Limit" if artist_name + "&%!" in check else "No Limit"))
        return check if check == "Artist_has_no_url" else jsonify(get_artist_songs(artist_name, "Limit" if artist_name + "&%!" in check else "No Limit")), 202


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


""" Method select_single_song
    Chooses one random song from a list
    @param song_list list of songs in format (song name - url)
    @return a single song from the list (in the same format)
"""


def select_single_song(song_list):
    return random.choice(song_list)


""" Method song_autofill
    cem...
"""


def song_autofill(song_list, user_input):
    names_list = []
    final_list = []

    for i in range(len(song_list)):
        names_list.append(song_list[i].split("-")[0])

    for i in range(len(names_list)):
        if names_list[i].lower().strip().__contains__(user_input.lower()):
            final_list.append(names_list[i])

    return final_list


def get_artist_songs(artist_name, blank_space):
    songs_list = []  # creates list for all artist that include the given 'artist_name' in their names
    artist_list = []  # creates list for songs of the chosen artist

    results = spotifyObject.search(q=artist_name, type='artist')  # gets the artists from spotify

    for item in results['artists']['items']:  # Adds the artist names to the list
        artist_list.append(item['name'])

    results = spotifyObject.search(q="artist:" + artist_list[0], type='track',
                                   limit=50)  # gets 50 songs from artists that include 'given artist' in their name

    for track in results['tracks']['items']:
        song_name = track['name']  # gets the name of the song
        preview_url = track['preview_url']  # gets the url of the song

        artist_check = track['artists'][0]['name']  # gets the artist of the song from song url

        if song_name and preview_url and artist_check.lower().strip() == artist_name.lower().strip():
            songs_list.append(
                song_name + "-" + preview_url)  # checks if the artist of the song is the needed one and creates a list with the name+url

    songs_list = []
    artist_list = []
    if blank_space == "Limit":
        songs_list.append("Limited Selection")
    elif blank_space == "No Limit":
        songs_list.append("")

    results = spotifyObject.search(q=artist_name, type='artist')

    for item in results['artists']['items']:
        artist_list.append(item['name'])

    results = spotifyObject.search(q="artist:" + artist_list[0], type='track', limit=50)

    for track in results['tracks']['items']:
        song_name = track['name']
        preview_url = track['preview_url']

        artist_check = track['artists'][0]['name']

        if song_name and preview_url and artist_check.lower().strip() == artist_name.lower().strip():
            songs_list.append(f"{song_name}-{preview_url} ")

    return songs_list


"""
"""


def artist_check(artist_name):
    if len(get_artist_songs(artist_name, "")) >= 10:
        return artist_name  # if artist has more than 10 playable songs, returns artist

    elif len(get_artist_songs(artist_name, "")) < 10 and len(get_artist_songs(artist_name, "")) > 0:
        return artist_name + "&%!", len(get_artist_songs(artist_name, ""))  # if artist has between 1 and 10 playable
        # songs, returns a different code that will allow a pop up disclaimer warning the player about the small song
        # amount. Returns length of song list.

    else:
        no_url = "Artist_has_no_url"
        return no_url  # if artist has no playable songs, returns an error


def calculate_score(guess_time, streak,
                    previous_score):  # insert guess time in ms, streak and total score from other rounds(if it is the
    # first round, give 0)

    org_point = 1000
    streak_multiplier = 1.02  # the score will get multiplied by the multiplier^streak
    time_penalty = guess_time / 2  # the points that will be subtracted from org_point

    point = (org_point - time_penalty) * streak_multiplier ^ streak  # calculates point earned from only the last song
    total_point = point + previous_score  # calculates the total point of player

    return total_point, point  # returns final point for total


def get_img_link(artist_name):
    results = spotifyObject.search(q='artist:' + artist_name, type='artist')

    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        return artist['images'][0]['url']
