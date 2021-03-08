from channels import Channel
from dateutil.parser import parse
import requests
import json
import time

# BuildPlaylist
# Loops through a set of channels and adds their videos to a predefined playlist
# Only one video can be inserted at a time, and has a cost of 50 units per request
# The number of requests should be limited using the MaxRequests setting to avoid
# quota errors
# Params
# channels: list of channels containing lists of videos to add
# settings: reference to the settings object
# Output
# No return value. If an error occurs for a channel, the last successfull video will be stored
# in the channel object and the rest of the channel's videos will be skipped. It is advised to
# write the updated channel date to disk or manually overwrite the previous channel date setting
# to avoid duplicating videos in the playlist.
def BuildPlaylist(channels,settings):
    videoCount = countVideos(channels)
    n = min(settings.MaxVideos,videoCount)
    for c in channels:
        nVids = len(c.Videos)
        count = min(n,nVids)
        dumpVideos(count,c,settings)
        n = n - nVids
        if n <= 0:
            break

def countVideos(channels :Channel):
    count = 0
    for c in channels:
        count = count + len(c.Videos)
    return count

def dumpVideos(count, channel, settings):
    lastDate = ""
    end = len(channel.Videos) - 1
    for i in range(count):
        index = end - i
        print(f'index={index}')
        data = getJson(channel,channel.Videos[index],settings)
        query = {'part':'snippet', 'key':settings.APIKey}
        headers = {
            'Authorization':f'Bearer {settings.Token()}',
            'Accept':'application/json',
            'Content-Type':'application/json'
        }
        response = requests.post("https://youtube.googleapis.com/youtube/v3/playlistItems",
            params=query,headers=headers,json=data)
        if response.status_code != 200:
            print(f"Failed to insert video: {channel.Videos[index]['contentDetails']['videoId']}") 
            print(response.text)
            break
        else:
            lastDate = channel.Videos[index]['contentDetails']['videoPublishedAt']
            time.sleep(0.5)
    if lastDate != "":
        channel.LastUploadDate = parse(lastDate)

def getJson(channel,video,settings):
    data = {
        "snippet": {
            "playlistId": settings.PlaylistID,
            "resourceId": {
                "kind":"youtube#video",
                "videoId": video["contentDetails"]["videoId"]
            }
        }
    }
    return data
        


