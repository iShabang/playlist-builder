import requests
import webbrowser
import os
import reading
import writing
import building
from settings import Settings
from server import OathResponseListener

def getPermission(clientID):
    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    pDict = {
        f"?client_id={clientID}":"",
        "&redirect_uri=http://127.0.0.1:8080":"",
        "&response_type=code":"",
        "&scope=https://www.googleapis.com/auth/youtube":""
    }
    params = list(pDict.keys())
    request = "".join((url,*params))
    webbrowser.open_new_tab(request)
    listener = OathResponseListener("127.0.0.1",8080)
    return listener.content

def getFirstToken(id, secret, code):
    url = 'https://oauth2.googleapis.com/token'
    body = {
        "client_id":id,
        "client_secret":secret,
        "code":code,
        "grant_type":"authorization_code",
        "redirect_uri":"http://127.0.0.1:8080"
    }
    response = requests.post(url,data=body)
    if response.status_code == 200:
        return response.json()['access_token']
    return ""

if __name__ == '__main__':
    settings = Settings()
    accessCode = getPermission(settings.ClientID)
    token = getFirstToken(settings.ClientID, settings.ClientSecret, accessCode)
    print(f'Token: {token}')
    settings.SetToken(token)
    channels = reading.ReadChannels('channels.json',settings) 
    for ch in channels:
        ch.GetVideoList()
    building.BuildPlaylist(channels, settings)
    writing.WriteChannels('channels.json',channels)

    
