"""
# import statements
import requests
from operator import itemgetter
from twilio.rest import Client
from picamera import PiCamera
import sys
import json
import os
import urllib, httplib, base64, json
import boto3
import datetime
import time
import RPi.GPIO as GPIO
import time 


# -----declare all the APIS, Keys, and Static Variables------ #
BaseDirectory = '/home/pi/Projects/Photos/' # directory where picamera photos are stored
KEY = '7373da1d38e540f3b579bf3e0f8154c3'# authorization key for azure
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'

account_sid = 'AC2b7b24efed2b931eae736299db0b6d69' # twilio sid
auth_token = '990e4e9094bf5fb1d92920074aea0f4e' # twilio authorization token

group_id = 'family' # name of personGroup


# ------Setup Camera module and the Motion Sensor------ #

#*****Raspberry Pi pin setup*****#
Blue = 11
Red = 12
Green = 13
Pir= 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Pir, GPIO.IN)

#*****Camera Setup*****#
camera = PiCamera() # initiate camera
camera.rotation = 180 # Used to correct orientation of camera

#*****FUNCTIONS*****#

# LED on off functions
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
    
    
    

# --------Face Recognition---------- #
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


# ------Twillio------#
    def twilio(message, imageLink):
    client = Client(account_sid, auth_token)

    message = client.messages.create(to='<destination phone number>', from_='<Your twilio phone number>', body = message)



# MAIN

while loop:
    peopleLists
    necessary Variables
    
    if motion not detected:
        ledOff()
        sleep()
    elif motion detected == 1:
        # create a directory to store images
        ledOn()
        #start camera and take pictures
        camera.capture("directory".jpg)
        sleep(x) # take a photo every x seconds
        
        # iterate through directory and detect faces
        detectFaces()
        # identify faces and updates the peopleLists 
        identifyFaces()
        gets details
        if face_is_identified:
            timer = startTimer()
            dict = {"Name of the person identified":timer}
            while timer < the time:
                if motion not present:
                    reset
                    break;
                sleep(x) # sleeps for x seconds
            if motion present:
                if face is still present:
                    message() # messages that the person is in the kitchen for x long
                else:
                    reset and break 
        else:
            message saying that an intruder is stealing food from the kitchen
        sleep(x) before looking for motion again
        
            
        
         
    





"""