from flask import Flask, render_template, request, flash, redirect, session, g
import sqlite3
import re
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_request
def before_request():
    g.db = sqlite3.connect("karaoke.db")
    g.db.row_factory = sqlite3.Row
    
    
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
@login_required
def index():
    """ Show all karaoke songs. """
    
    cur = g.db.cursor()
    cur.execute('SELECT * FROM songs WHERE user_id = ?', (session['user_id'],))
    songs = [dict(song) for song in cur.fetchall()]
    return render_template('index.html', active_page='home', songs=songs)


@app.route('/details/<int:id>')
@login_required
def details(id):
    """ Show details for a specific karaoke song. """
    
    cur = g.db.cursor()
    cur.execute('SELECT * FROM songs WHERE id = ?', (id,))
    song = dict(cur.fetchone())
    
    # Craft embed URLs
    pattern = r"(?<=v=)[^&#]+"
    match = re.search(pattern, song['karaoke_video_url'])
    if match:
        song["karaoke_video_url"] = f"https://www.youtube.com/embed/{match.group()}"
    match = re.search(pattern, song['lyrics_video_url'])
    if match:
        song["lyrics_video_url"] = f"https://www.youtube.com/embed/{match.group()}"
    return render_template('details.html', active_page='details', song=song)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_karaoke():
    """ Add a new karaoke song to the database. """
    
    if request.method == 'POST':
        song = request.form.get('song')
        artist = request.form.get('artist')
        
        if not song:
            flash('Song is required!')
            return redirect('/new')
        elif not artist:
            flash('Artist is required!')
            return redirect('/new')
        
        karaoke_video_url = request.form.get('karaoke-video-url')
        if not karaoke_video_url:
            karaoke_video_url = ""
        lyrics_video_url = request.form.get('lyrics-video-url')
        if not lyrics_video_url:
            lyrics_video_url = ""
        lyrics = request.form.get('lyrics')
        if not lyrics:
            lyrics = ""
        
        cur = g.db.cursor()
        cur.execute('INSERT INTO songs (user_id, song, artist, karaoke_video_url, lyrics_video_url, lyrics) VALUES(?, ?, ?, ?, ?, ?)', (session['user_id'], song, artist, karaoke_video_url, lyrics_video_url, lyrics))
        g.db.commit()
        return redirect('/')
    else:
        return render_template('new-karaoke.html', active_page='new-karaoke')
    
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_karaoke(id):
    """ Edit a karaoke song in the database. """
    if request.method == 'POST':
        song = request.form.get('song')
        artist = request.form.get('artist')
        
        if not song:
            flash('Song is required!')
            return redirect('/edit/' + str(id))
        elif not artist:
            flash('Artist is required!')
            return redirect('/edit/' + str(id))
        
        karaoke_video_url = request.form.get('karaoke-video-url')
        if not karaoke_video_url:
            karaoke_video_url = ""
        lyrics_video_url = request.form.get('lyrics-video-url')
        if not lyrics_video_url:
            lyrics_video_url = ""
        lyrics = request.form.get('lyrics')
        if not lyrics:
            lyrics = ""
        
        cur = g.db.cursor()
        cur.execute('UPDATE songs SET song = ?, artist = ?, karaoke_video_url = ?, lyrics_video_url = ?, lyrics = ? WHERE id = ?', (song, artist, karaoke_video_url, lyrics_video_url, lyrics, id))
        g.db.commit()
        return redirect('/')
    else:
        cur = g.db.cursor()
        cur.execute('SELECT * FROM songs WHERE id = ?', (id,))
        song = dict(cur.fetchone())
        return render_template('edit-karaoke.html', active_page='edit-karaoke', song=song)
    

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_karaoke(id):
    """ Delete a karaoke song from the database. """
    
    cur = g.db.cursor()
    cur.execute('DELETE FROM songs WHERE id = ?', (id,))
    g.db.commit()
    return redirect('/')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('username is required!')
            return redirect('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('password is required!')
            return redirect('/login')

        # Query database for username
        cur = g.db.cursor()
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid username and/or password')
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        if session.get('user_id'):
            return redirect('/')
        return render_template("login.html")
    
    
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            flash('username is required!')
            return redirect('/register')

        # Ensure password was submitted
        if not request.form.get("password"):
            flash('password is required!')
            return redirect('/register')

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            flash('confirmation is required!')
            return redirect('/register')

        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            flash('password and confirmation must match!')
            return redirect('/register')

        # Ensure username doesn't exist already
        cur = g.db.cursor()
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        if len(rows) != 0:
            flash('username already exists!')
            return redirect('/register')

        # Create new user
        cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"))))
        user_id = cur.lastrowid
        g.db.commit()
    
        # Remember which user has logged in
        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("register.html")
