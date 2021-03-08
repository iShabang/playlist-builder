import io
import json
from channels import Channel

# WriteChannels
# Writes channel data in json format to disk
# Params
# filename: path to write to
# channels: list of channels
def WriteChannels(filename, channels):
    f = io.open(filename,'w')
    dataDict = {"channels":[]}
    for ch in channels:
        dataDict['channels'].append({'id':ch.PlaylistID,'lastDate':str(ch.LastUploadDate)})
    data = json.dumps(dataDict)
    f.write(data)
    f.close()
    
