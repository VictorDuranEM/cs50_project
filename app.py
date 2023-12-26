from flask import Flask, render_template, request, flash, redirect, session, g
import sqlite3
from flask_session import Session

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
def index():
    cur = g.db.cursor()
    cur.execute('SELECT * FROM songs')
    songs = [dict(song) for song in cur.fetchall()]
    return render_template('index.html', active_page='home', songs=songs)

@app.route('/new', methods=['GET', 'POST'])
def new_karaoke():
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
        cur.execute('INSERT INTO songs (song, artist, karaoke_video_url, lyrics_video_url, lyrics) VALUES (?, ?, ?, ?, ?)', (song, artist, karaoke_video_url, lyrics_video_url, lyrics))
        g.db.commit()
        return redirect('/')
    else:
        return render_template('new-karaoke.html', active_page='new-karaoke')
    
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_karaoke(id):
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
def delete_karaoke(id):
    cur = g.db.cursor()
    cur.execute('DELETE FROM songs WHERE id = ?', (id,))
    g.db.commit()
    return redirect('/')