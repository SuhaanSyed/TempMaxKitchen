import urllib, httplib, base64, json

group_id = 'family'

KEY = '7373da1d38e540f3b579bf3e0f8154c3'
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'


headers = {'Ocp-Apim-Subscription-Key': KEY}
params = urllib.urlencode({'personGroupId': group_id})
conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
conn.request("GET", (ENDPOINT+"/face/v1.0/persongroups/"+group_id+"/training?%s") % params, "{body}", headers)
response = conn.getresponse()
data = json.loads(response.read())
print(data)
conn.close()