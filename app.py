from flask import Flask, render_template
from flask_session import Session

from helpers import top_songs, allow_user, top_artists, read_playlists, currently_listening

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    global user
    user = None
    return render_template("homepage.html", user=user)

@app.route("/shortsongs")
def shortsongs():
    songs_short, songs_medium, songs_long = top_songs(user)
    return render_template("songs.html", heading="top songs (last month)", songs=songs_short)

@app.route("/mediumsongs")
def mediumsongs():
    songs_short, songs_medium, songs_long = top_songs(user)
    return render_template("songs.html", heading = "top songs (last six months)", songs=songs_medium)

@app.route("/longsongs")
def longsongs():
    songs_short, songs_medium, songs_long = top_songs(user)
    return render_template("songs.html", heading = "top songs (all time)", songs=songs_long)

@app.route("/shortartists")
def shortartists():
    artists_short, artists_medium, artists_long = top_artists(user)
    return render_template("artists.html", heading="top artists (last month)", artists=artists_short)

@app.route("/mediumartists")
def mediumartists():
    artists_short, artists_medium, artists_long = top_artists(user)
    return render_template("artists.html", heading="top artists (last six months)", artists=artists_medium)

@app.route("/longartists")
def longartists():
    artists_short, artists_medium, artists_long = top_artists(user)
    return render_template("artists.html", heading="top artists (all time)", artists=artists_long)

@app.route("/allow")
def allow():
    global user
    user = allow_user()
    return render_template('homepage.html', user=user)

@app.route("/logout")
def logout():
    user = None
    return render_template('homepage.html', user=user)

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/playlists")
def playlists():
    playlists = read_playlists(user)
    return render_template('playlists.html', playlists=playlists)

@app.route("/listening")
def listening():
    listening = currently_listening(user)
    return render_template("listening.html", listening=listening)