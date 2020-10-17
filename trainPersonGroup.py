import urllib, httplib, base64
import json

group_id = 'family'
KEY = '7373da1d38e540f3b579bf3e0f8154c3'
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'



params = urllib.urlencode({'personGroupId': group_id})
headers = {'Ocp-Apim-Subscription-Key': KEY}

conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
conn.request("POST", (ENDPOINT+"/face/v1.0/persongroups/family/train?%s") % params, "{body}", headers)
response = conn.getresponse()
data = json.loads(response.read())
print(data) # if successful prints empty json body