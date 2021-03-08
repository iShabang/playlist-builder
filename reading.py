import io
import json
from channels import Channel

# ReadChannels
# Reads channel data from disk and returns a list of channel objects
# Params
# filename: path to the file containing the data. Must be in json format.
# settings: reference to the settings object
# Return: List of Channel objects
def ReadChannels(filename,settings):
    data = readData(filename)
    channels = list()
    for ch in data["channels"]:
        channels.append(Channel(ch['id'],ch['lastDate'],settings))
    return channels

# ReadSettings
# Reads settings data from disk and returns a dictionary of settings values
# Params
# filename: path to the file containing settings data
# Return: dictionary of settings
def ReadSettings(filename):
    data = readData(filename)
    return data

def readData(filename):
    f = io.open(filename, "r")
    text = f.read()
    data = json.loads(text)
    f.close()
    return data