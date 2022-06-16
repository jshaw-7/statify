import os
from cs50 import SQL

from flask import redirect, render_template, request, session

import sys
import spotipy
import spotipy.util as util

from spotipy.oauth2 import SpotifyOAuth

global sp

client_id ='b02eba6bbf4a48a484c525c15555b616'
client_secret = '3b9d813cd07e4bc5acfa39c3c3659dce'
redirect_uri = "http://localhost:8080/callback"

def top_songs(sp):
    scope = 'user-top-read'

    songs_short = []
    songs_medium= []
    songs_long=[]

    short = sp.current_user_top_tracks(time_range='short_term', limit=50)
    for i, item in enumerate(short['items']):
        songs_short.append([str(i+1)+ '. ' +item['name']+ ' // '+ item['artists'][0]['name'], item['external_urls']['spotify']])
    medium = sp.current_user_top_tracks(time_range='medium_term', limit=50)
    for i, item in enumerate(medium['items']):
        songs_medium.append([str(i+1) + '. ' +item['name']+ ' // '+ item['artists'][0]['name'], item['external_urls']['spotify']])
    lng = sp.current_user_top_tracks(time_range='long_term', limit=50)
    for i, item in enumerate(lng['items']):
        songs_long.append([str(i+1) + '. ' +item['name'] + ' // ' + item['artists'][0]['name'], item['external_urls']['spotify']])

    return songs_short, songs_medium, songs_long

def allow_user():
    scope = 'user-top-read playlist-read-private user-read-currently-playing'

    token = util.prompt_for_user_token(scope, client_id = client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    if token:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = scope, client_id = client_id,
                            client_secret = client_secret, redirect_uri = redirect_uri))
    else:
        sp = None
    return sp

def top_artists(sp):
    scope = 'user-top-read'

    artists_short = []
    artists_medium= []
    artists_long=[]

    short = sp.current_user_top_artists(time_range='short_term', limit=10)
    for i, item in enumerate(short['items']):
        artists_short.append([str(i+1)+ '. ' +item['name'], item['external_urls']['spotify']])
    medium = sp.current_user_top_artists(time_range='medium_term', limit=10)
    for i, item in enumerate(medium['items']):
        artists_medium.append([str(i+1) + '. ' +item['name'], item['external_urls']['spotify']])
    lng = sp.current_user_top_artists(time_range='long_term', limit=10)
    for i, item in enumerate(lng['items']):
        artists_long.append([str(i+1) + '. ' +item['name'], item['external_urls']['spotify']])

    return (artists_short, artists_medium, artists_long)

def read_playlists(sp):
    scope = 'playlist-read-private'
    playlists = []
    results = sp.current_user_playlists(limit=50)
    for i, item in enumerate(results['items']):
        playlists.append([str(i+1)+'.  '+ item['name'], item['external_urls']['spotify']])
    return playlists

def currently_listening(sp):
    scope = 'user-read-currently-playing'
    results = sp.currently_playing()
    if results:
       return [results['item']['name'] + ' // ' + results['item']['artists'][0]['name'], results['item']['external_urls']['spotify']]
    else:
        return ['not currently listening to anything.', ]

