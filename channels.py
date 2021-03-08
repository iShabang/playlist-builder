import requests
from datetime import datetime
from dateutil.parser import parse

# Class: Channel
# Stores information about a youtube channel and can fetch video lists for that channel
# The term "channel" is more of an abstraction. This class is really information
# about the "uploads" playlist for a specific channel. Hence the PlaylistID member variable.
# However, it is easier to think of each list of videos as a reference to a specific channel.
class Channel(object):
    # Constructor
    # Params
    # id: the id for this channel's "uploads" playlist
    # lastUploadDate: The upload date of the last video from this channel that was watched or added
    # to the playlist 
    # settings: Reference to the settings object
    def __init__(self, id, lastUploadDate, settings):
        self.PlaylistID = id
        self.LastUploadDate = parse(lastUploadDate,ignoretz=True)
        self._settings = settings
        self.Videos = list()

    # GetVideoList
    # Fetches and returns all the videos in the channel's "uploads" playlist that are newer than the
    # LastUploadDate
    # Output: No output. Videos are populated in Channel.Videos
    def GetVideoList(self):
        token = ""
        done = False
        while not done:
            response = self._fetchPage(token)
            if response.status_code == 200:
                data = response.json()
                done = self._processPage(data)
                if not done:
                    token = data['nextPageToken']
            else:
                print(f"Error getting videos for {self.PlaylistID}")
                print(response.status_code)
                print(response.text)
                break
    
    def _processPage(self,data :dict):
        videos = data['items']
        end = len(videos)
        done = False
        for i in range(len(videos)):
            date = parse(videos[i]['contentDetails']['videoPublishedAt'],ignoretz=True)
            if date <= self.LastUploadDate:
                done = True
                end = i
                break
        self.Videos.extend(videos[:end])
        return done

    def _fetchPage(self,token=""):
        query = {'part':'contentDetails', 'key':self._settings.APIKey, 'maxResults':50, 'playlistId':self.PlaylistID}
        if token != "":
            query['pageToken'] = token
        headers = {
            'Accept':'application/json'
        }
        return requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems',
            headers=headers,params=query)