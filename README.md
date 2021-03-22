# YouTube Playlist Builder
Simple application that grabs unwatched youtube videos from specified channels and adds them to a specified playlist. This makes it easier to keep track of all the videos you need to watch by consolidating everything into one playlist. This saves the time of manually adding each video by hand.

## Initial Setup

### Google Setup
You must start a project on the google developer console to obtain a valid API key, client id, and client secret. It is also the user's responsibility to properly estimate the quota usage and set the correct maximum request value for the application. Insertions are costly and large amounts of videos can quickly expend the daily quota cost if not careful.

### Virtual Environment (optional)
    python -m venv builder-env

### Install Dependencies
    pip install -r requirements.txt

### Settings
The playlist builder requires some information to make requests to the Youtube Data API. Values must be supplied in a settings.json file. Copy the following to a new file and name it settings.json. Then fill in the values.

    {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "playlist_id": "your_playlist_id",
        "api_key": "your_api_key",
        "max_videos": maximum_number_of_video_insertion_requests
    }

### Channel Information
Youtube channels to grab videos from must be specified in a channels.json. Each channel must have the id for its "uploads" playlist followed by the oldest upload date to pull videos from. Copy the following template and save it to a file named channels.json. Then fill in the values:

    {
        "channels":
        [
            {
                "id":"UUJ6td3C9QlPO9O_J5dF4ZzA",
                "lastDate":"2020-06-28 00:00:00"
            }
        ]
    }

## Usage
After initial setup start the builder with:

    python main.py

You will immediately be prompted by your webbrowser with a permission request from google. Follow the prompts to allow
the application to access your playlist. Once complete, the script will begin inserting videos into your selected playlist