import RPi.GPIO as GPIO
import time

Blue = 11
Red = 12
Green = 13
s1 = 16

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Blue, GPIO.OUT)
GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(s1, GPIO.IN, GPIO.PUD_DOWN)



def lightOff():
    GPIO.output(Red, 1)
    GPIO.output(Green, 1)
    GPIO.output(Blue, 1)
    time.sleep(.3)



def lightOn():
    GPIO.output(Red, 1)
    GPIO.output(Green, 1)
    GPIO.output(Blue, 1)
    time.sleep(.3)

while True: lightOn()
"""
while True:

    i = GPIO.input(s1)
    print(i)
    if i == 0:
        print("Nothing is moving")
        time.sleep(1)
        lightOff()
    elif i == 1:
        print("Motion Detected")
        #lightOn()
        time.sleep(2)



while True:
    x = int(input())
    if x == 1:
        lightOn()
    else:
        lightOff()
"""