import requests
import urllib, httplib, base64

KEY = '7373da1d38e540f3b579bf3e0f8154c3'
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'

group_id = 'family'
body = '{"name": "family"}'
params = urllib.urlencode({'personGroupId': group_id})
headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}

conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
conn.request("PUT", (ENDPOINT+"/face/v1.0/persongroups/family?%s") % params, body, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()