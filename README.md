# Karaoke Library

Welcome to the Karaoke Library, a Flask-based web application dedicated to managing and viewing a collection of karaoke songs. This application is designed to provide users with the functionalities to add, manage, and enjoy their favorite karaoke songs.

**Video Demo**:  <https://youtu.be/LOkwvP2b_T4>

## Project Structure

Below is the breakdown of the primary components:

`app.py`: This Python file orchestrates the web server using Flask, managing routes and integrating with other components of the application to serve content to the user.

`helpers.py`: This Python file contains helper funtions to be used by the application.

`static/styles/styles.css`: This Cascading Style Sheets (CSS) file defines the visual aspects of the application, ensuring a user-friendly and aesthetically pleasing interface.

`schema.sql`: This file contains the SQL schema defining the structure of the application's database, including tables and relationships essential for storing user data and karaoke song information.

`templates/`: A crucial directory, housing all the HTML templates. These templates are rendered by Flask and serve as the visual structure for the user interface.

The application incorporates Bootstrap within the templates/layout.html file to ensure a responsive and modern design. Bootstrap aids in creating a consistent look and feel across the platform while also speeding up the development process.

## Setting up the Karaoke Library

1. **Install Dependencies:** Begin by installing the necessary packages via `pip install -r requirements.txt.` This will ensure all the Python libraries and frameworks needed are at your disposal.
2. **Database Creation:** Utilize `sqlite3 karaoke.db` to create your application's database. This step initializes a new database that will store all the application data.
3. **Database Initialization:** Within the sqlite3 prompt, execute the commands found in schema.sql to construct the necessary tables and structures in the database.
4. **Run the Application:** Finally, launch the web application using the command `flask run --debug`. The debug flag aids in live development by reloading the server upon file changes and providing debug information.

## How to Use the Application

Once the application is running, users can engage with the following features:

* **User Registration/Login:** Secure user authentication allows users to have personal dashboards and manage their karaoke collection.
* **Karaoke Dashboard:** Users can add new karaoke songs, complete with song name, artist, lyrics, and links to YouTube videos - one for the instrumental version and another for the lyrical video.
* **Song Management:** Each song in the user's dashboard can be edited or deleted, providing full control over their collection.
* **Lyrics and Videos:** Clicking on a song title takes users to a dedicated page where they can view the lyrics and watch the associated YouTube videos.

## YouTube URL Conversion

An intuitive feature of the application is its ability to convert standard YouTube URLs into embeddable links. This means when users add a song by pasting a YouTube link, the application automatically transforms it into an embedded video URL directly viewable within the user interface.