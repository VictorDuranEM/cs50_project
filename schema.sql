CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song TEXT NOT NULL,
    artist TEXT NOT NULL,
    karaoke_video_url TEXT,
    lyrics_video_url TEXT,
    lyrics TEXT
);