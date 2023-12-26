# Karaoke App

This is a Flask-based web application for managing and viewing karaoke songs.

## Project Structure

- `app.py`: The main application file which uses Flask and jinja to render the HTML templates.
- `static/styles/styles.css`: The CSS styles for the application.
- `schema.sql`: The SQL schema for the application's database.
- `templates/`: This directory contains all the HTML templates used by the application.

The application also uses bootstrap, which is included in the `templates/layout.html` file.

## How to Run the Application

1. Install the required packages using `pip install -r requirements.txt`.
2. Create the database using `sqlite3 karaoke.db`.
3. While inside the sqlite3 prompt, create the tables described in `schema.sql`.
4. Still inside the sqlite3 prompt, run the following: `.headers on` and `.mode column` to make the output of the queries compatible with the application.
5. Run the application using `flask run --debug`.

## How to Use the Application

The application allows the user to register/login to the application and then add karaoke songs to their dashboard.
The karaoke songs can include the song name, artist, lyrics and links to 2 videos on YouTube. One for the karaoke version of the song and one for the lyrics video.

In the dashboard, the user can edit the karaoke songs they have added and delete them.

When clicking the name of a song in the dashboard, the user is taken to a page where they can view the lyrics and the videos for that song.

## YouTube URLs

The application internally converts the YouTube URLs to embed URLs, which are then used to embed the videos in the application.
