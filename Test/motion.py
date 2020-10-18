import RPi.GPIO as GPIO
sensorPin = 23 # the gpio pin number

#GPIO setup
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(sensorPin, GPIO.IN, GPIO.PUD_DOWN) # sets the pin number as input

if GPIO.input(sensorPin) == 1: # if motion is detected
  print("Initiate the camera")

else: # if not detected
  print("Don't do anything that")
