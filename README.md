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
3. While inside the sqlite3 prompt, create the table described in `schema.sql` inside the database.
4. Still inside the sqlite3 prompt, run the following: `.headers on` and `.mode column`.
5. Run the application using `flask run`.

## How to Use the Application

The application allows the user to 