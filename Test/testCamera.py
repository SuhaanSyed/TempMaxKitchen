from picamera import PiCamera
from time import sleep

base_directory = '/home/pi/Projects/camera_test/'

camera = PiCamera() 
for i in range(10):
    test_input = input("Do you want to take a pic? (yes/no)")
    if test_input == "yes":
        camera.capture(base_directory + str(i) +'.jpg')