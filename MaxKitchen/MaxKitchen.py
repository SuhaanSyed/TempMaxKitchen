# MadMaxKitchen.py 
import requests
from operator import itemgetter
from twilio.rest import Client
from picamera import PiCamera
import sys
import json
import os
import urllib, httplib, base64, json
from datetime import datetime
import time
from time import sleep
import RPi.GPIO as GPIO

# *** Declare all keys and apis **** #
KEY = '7373da1d38e540f3b579bf3e0f8154c3'
ENDPOINT = 'https://madmaxfacialrecognition.cognitiveservices.azure.com/'
group_id = 'family'
account_sid = 'AC2b7b24efed2b931eae736299db0b6d69'
auth_token = '990e4e9094bf5fb1d92920074aea0f4e'
BaseDirectory = '/home/pi/Projects/MaxKitchen/photo dump/'
checkDirectory = '/home/pi/Projects/MaxKitchen/checkDirectory/'
location = "Kitchen"
# *** Limits *** #
maxNotPresent = 6
maxTime = 15

# *** GPIO SETUP *** #

buzzer = 17
sensor1 = 23
sensor2 = 27
ledPins = [22, 25, 12]

GPIO.setwarnings(0)


def setup():
    global pwmRed, pwmGreen, pwmBlue
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPins, GPIO.OUT)
    GPIO.output(ledPins, GPIO.HIGH)
    pwmRed = GPIO.PWM(ledPins[0], 2000)
    pwmGreen = GPIO.PWM(ledPins[1], 2000)
    pwmBlue = GPIO.PWM(ledPins[2], 2000)
    pwmRed.start(0)
    pwmGreen.start(0)
    pwmBlue.start(0)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(sensor1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sensor2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# *** Led Functions *** #
def setColor(r, g, b):
    pwmRed.ChangeDutyCycle(r)
    pwmGreen.ChangeDutyCycle(g)
    pwmBlue.ChangeDutyCycle(b)


# *** Camera Setup *** #
camera = PiCamera()

# *** Face Recognition ***"""
"""
all the facial recognition is done by the following four methods
> iter, detect, identifyFaces, getName
"""


# 1) iterates through the given directory
# 2) finds .jpg files
# 3) sends them to detect faces
# 4) dir = directory, check = which type of directory (regular / overtime)

def iterate(dir, check):
    for fileName in os.listdir(dir):
        if fileName.endswith('.jpg'):
            filePath = os.path.join(dir, fileName)
            fileList.append(filePath)
            tempIdList = detect_faces(filePath)
            if check:
                for id in tempIdList:
                    checkOvertime.append(id)
            else:
                print("did I come here? ")
                for id in tempIdList:
                    faceIdList.append(id)
                    print(len(faceIdList))


# detects faces in images from previously using azure post request
def detect_faces(img_dir):
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}
    body = open(img_dir, 'rb')

    params = urllib.urlencode({'returnFaceId': 'true'})

    connection = httplib.HTTPSConnection(
        'northcentralus.api.cognitive.microsoft.com')  # "northcentralus" will change depending on ENDPOINT
    connection.request("POST", (ENDPOINT + 'face/v1.0/detect?%s') % params, body,
                       headers)  # this is the specific endpoint
    response = connection.getresponse()
    photo_data = json.loads(response.read())
    tempId = []  # a temporary id list is used here to prevent conflicts between regular vs. overtime facial recognition
    if not photo_data:  # empty post is the indication of no face
        print('No face identified')
    else:  # if face is found
        for face in photo_data:  # for the faces identified in each photo
            tempId.append(str(face['faceId']))  # get faceId for use in identify
    return tempId


# Takes in list of faceIds and uses azure post request to match face to known faces
def identify_faces(ids):
    if not faceIdList:  # if list is empty, no faces found in photos
        result = [('n', .0), 'n']  # create result with 0 confidence
        return result  # return result for use in main
    else:  # potential match 
        headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}
        params = urllib.urlencode({'personGroupId': group_id})
        body = "{'personGroupId':'family', 'faceIds':" + str(ids) + ", 'confidenceThreshold': '.5'}"
        connection = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
        connection.request("POST", (ENDPOINT + "/face/v1.0/identify?%s") % params, body, headers)
        response = connection.getresponse()

        data = json.loads(response.read())

        for resp in data:
            candidates = resp['candidates']
            for candidate in candidates:  # for each candidate in the response
                confidence = candidate['confidence']  # retrieve confidence
                personId = str(candidate['personId'])  # and personId
                confidenceList.append((personId, confidence))
        connection.close()
        SortedconfidenceList = zip(confidenceList, fileList)  # merge fileList and confidence list
        sortedConfidence = sorted(SortedconfidenceList, key=itemgetter(1))  # sort confidence list by confidence
        return sortedConfidence[-1]  # returns tuple with highest confidence value (sorted from smallest to biggest)


# takes in person_id and retrieves known person's name with azure GET 
def get_name(person_Id):
    print("Called GetName")
    headers = {'Ocp-Apim-Subscription-Key': KEY}
    params = urllib.urlencode({'personGroupId': group_id, 'personId': person_Id})

    connection = httplib.HTTPSConnection('northcentralus.api.cognitive.microsoft.com')
    connection.request("GET",
                       (ENDPOINT + "/face/v1.0/persongroups/" + group_id + "/persons/" + person_Id + "?%s") % params,
                       "{body}", headers)
    response = connection.getresponse()
    data = json.loads(response.read())
    name = data['name']
    connection.close()
    return name


# *** Twillio Setup *** #
"""
Twillio is used to send text messages
"""


def twillio(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to='9137497489',
                                     from_='+12058983945',
                                     body=message)


# Calculates the total time spent
def totalTime(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    toS = list(map(str, [hours, mins, sec]))
    total = ":".join(toS)
    return total


# Cleans the GPIO pins
def destroy():
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()


detected = 1  # motion detected = 1
notDetected = 0  # motion not detected = 0
motionCount = 0
checkIter = 0

setup()  # used to set up the GPIO
print("program is starting")

sleep(5)
while True:
    fileList = []  # all the directories of the pictures go here
    faceIdList = []  # all the faceIds from DETECT go here; these are used in Identify Faces
    confidenceList = []  # confidence values of all faces go here
    motion = max(GPIO.input(sensor1), GPIO.input(sensor2))  # checks if motion is present
    if motion == notDetected:  # does nothing if motion is not present
        setColor(0, 0, 0)
        print("The area is clear")
    elif motion == detected:
        motionCount += 1
        picDirectory = BaseDirectory + str(motionCount) + '/'  # sets the directory
        setColor(100, 0, 0)
        os.mkdir(picDirectory)  # makes a new directory to store pictures
        # captures 4 photos
        for num_photos in range(4):
            date = datetime.now().strftime('%m_%d_%Y_%M_%S_')  # records the time and date of the picture
            camera.capture(picDirectory + date + '.jpg')
            sleep(2)

        # iterate through directory and detect faces
        iterate(picDirectory, False)  # False is used here because this is a regular face check
        # identify faces and updates the peopleLists

        if len(faceIdList) > 0:  # if tehre are faces then the faces are sent to identifyFaces
            result = identify_faces(faceIdList)  # confidence value along with faceId

            if result[0][1] > .65:  # if confidence is greater than 65% then getName is called
                name = get_name(result[0][0])
                print(name + " is in the " + location)
                twillio(name + " is in the " + location)
                now = datetime.now()  # starts the timer

                notPresentCount = 0  # motion not present Count
                while ((datetime.now() - now).seconds < maxTime):  # waits for overtime                 
                    motion = max(GPIO.input(sensor1), GPIO.input(sensor2))  # periodically checks for motion
                    if motion == notDetected:
                        print("Not Detected")
                        notPresentCount += 1
                    if notPresentCount > maxNotPresent:  # if the person is not present for most of the time, then the program resets
                        twillio(name + " left the " + location)
                        break
                    sleep(2)

                checkOvertime = []
                motionStillPresent = []
                for i in range(25):  # checks for any signs of motion for 25 times
                    motion = max(GPIO.input(sensor1), GPIO.input(sensor2))
                    motionStillPresent += [motion]

                if motionStillPresent.count(1) / len(
                        motionStillPresent) >= .6:  # declares overtime for motion present for more than 60%
                    checkIter += 1
                    tempCheckDirectory = checkDirectory + "/" + str(checkIter) + "/"
                    for check in range(5):
                        dir = tempCheckDirectory + str(check) + ".jpg"
                        camera.capture(dir)
                        sleep(2)
                    iterate(tempCheckDirectory, True)  # True is used to indicate overtime-facial recognition
                    if len(checkOvertime) > 0:  # if checkOvertime list is not empty
                        if name == get_name(identify_faces(checkOvertime)[0][0]):  # if name matches to initial name
                            msg = name + " crossed their time limit in the kitchen. They spent about " + totalTime((
                                                                                                                               datetime.now() - now).seconds) + " in the " + location + ". Please ask them to get out of there!"
                            GPIO.output(buzzer, GPIO.HIGH)
                            sleep(5)
                            GPIO.output(buzzer, GPIO.LOW)
                            twillio(msg)  # send the message
                    else:  # if the person left, then clear the space
                        break

                if notPresentCount > maxNotPresent:
                    break
            else:
                msg = "Burglar Burglar Burlar!!!"
                twillio(msg)
        else:
            print("No Faces in the list")
    print("Resetting")
    print("-" * 10)
    setColor(0, 0, 0)
    sleep(15)

