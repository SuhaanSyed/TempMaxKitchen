# MadMaxKitchen.py 
import requests
from operator import itemgetter
from twilio.rest import Client
from picamera import PiCamera
import sys
import json
import os
import urllib, httplib, base64, json
import datetime
import time
from time import sleep
import RPi.GPIO as GPIO



KEY = '7373da1d38e540f3b579bf3e0f8154c3'
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'
BaseDirectory = '/home/pi/Projects/facerecognitiontest/'
group_id = 'family'
fileList = []
faceIdList = [] # list for face id's generated using api - detect
confidenceList = [] # list of confidence values derived from api - identify

Blue = 11
Red = 12
Green = 12
s1 = 16
s2 = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(s1, GPIO.IN)
GPIO.setup(s2, GPIO.IN)

camera = PiCamera()

def lightOff():
    GPIO.output(Red, 1)
    GPIO.output(Green, 1)
    GPIO.output(Blue, 1)
    time.sleep(.3)



def lightOn():
    GPIO.output(Red, 0)
    GPIO.output(Green, 0)
    GPIO.output(Blue, 0)
    time.sleep(.3)


def iter():
    for fileName in os.listdir(BaseDirectory):
        if fileName.endswith('.jpg'):
            filePath = os.path.join(BaseDirectory, fileName) # joins directory path with filename to create file's full path
            fileList.append(filePath)
            #print(fileList)
            detect(filePath)


# detects faces in images from previously stated directory using azure post request
def detect(img_url):
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}
    body = open(img_url,'rb')

    params = urllib.urlencode({'returnFaceId': 'true'})

    
    conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')# this should be taken from your endpoint
    conn.request("POST", (ENDPOINT+'face/v1.0/detect?%s') % params, body, headers) # this is the specific endpoint
    response = conn.getresponse()
    photo_data = json.loads(response.read())
    #photo_data = json.loads(response.read())

    #print(photo_data)

    if not photo_data: # if post is empty (meaning no face found)
        print('No face identified')
    else: # if face is found
        for face in photo_data: # for the faces identified in each photo
            faceIdList.append(str(face['faceId'])) # get faceId for use in identify

# Takes in list of faceIds and uses azure post request to match face to known faces
def identify(ids):
    if not faceIdList: # if list is empty, no faces found in photos
        result = [('n', .0), 'n'] # create result with 0 confidence
        return result # return result for use in main
    else: # else there is potential for a match
        headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}
        params = urllib.urlencode({'personGroupId': group_id})
        body = "{'personGroupId':'family', 'faceIds':"+str(ids)+", 'confidenceThreshold': '.5'}"
        conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
        conn.request("POST", (ENDPOINT+"/face/v1.0/identify?%s") % params, body, headers)
        response = conn.getresponse()

        data = json.loads(response.read()) # turns response into index-able dictionary

        for resp in data:
            candidates = resp['candidates']
            for candidate in candidates: # for each candidate in the response
                confidence = candidate['confidence'] # retrieve confidence
                personId = str(candidate['personId']) # and personId
                confidenceList.append((personId, confidence))
        conn.close()
        SortedconfidenceList = zip(confidenceList, fileList) # merge fileList and confidence list
        sortedConfidence = sorted(SortedconfidenceList, key=itemgetter(1)) # sort confidence list by confidence
        return sortedConfidence[-1] # returns tuple with highest confidence value (sorted from smallest to biggest)


# takes in person_id and retrieves known person's name with azure GET 
def getName(person_Id):
    headers = {'Ocp-Apim-Subscription-Key': KEY}
    params = urllib.urlencode({'personGroupId': group_id, 'personId': person_Id})

    conn = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
    conn.request("GET", (ENDPOINT+"/face/v1.0/persongroups/"+group_id+"/persons/"+person_Id+"?%s") % params, "{body}", headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    name = data['name']
    conn.close()
    return name

    
    


lightOff()

while True:
    i = GPIO.input(s1)
    k = GPIO.input(s2)
    i = max(i,k)
    if i == 1:
        lightOn()
        sleep(20)
        for num_photos in range(4):
            camera.capture(BaseDirectory + str(c+num_photos) +'.jpg')
            sleep(2)
        iter()
        result = identify(faceIdList)

        if result[0][1] > .5:
            print(getName(result[0][0]))
        else:
            print("Not Recognised ")
    elif i == 0:
        lightOff()
        
            
    sleep(2)
    c+=1
    lightOff()
        
       
   









