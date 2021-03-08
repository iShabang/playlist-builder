from reading import ReadSettings

# Class: Settings
# Holds user setting values. Constructs the values using a settings.json file
class Settings(object):
    def __init__(self):
        data = ReadSettings("settings.json")
        self.ClientID = data["client_id"]
        self.ClientSecret = data["client_secret"]
        self.APIKey = data["api_key"]
        self.MaxVideos = data["max_videos"]
        self.PlaylistID = data["playlist_id"]
        self._token = ""
    
    # SetToken
    # Set the oath authorization token for future requests
    def SetToken(self,token):
        if self._token == "":
            self._token = token
    
    # Token
    # Return the oath authorization token as str
    def Token(self):
        return self._token