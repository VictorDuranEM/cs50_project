CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    song TEXT NOT NULL,
    artist TEXT NOT NULL,
    karaoke_video_url TEXT,
    lyrics_video_url TEXT,
    lyrics TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);