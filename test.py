import sys
import spotipy
import spotipy.util as util
from cs50 import SQL

from spotipy.oauth2 import SpotifyOAuth

db = SQL("sqlite:///users.db")

print(songs_short)