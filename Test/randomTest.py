import RPi.GPIO as GPIO
from time import sleep

led = 21
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led, GPIO.OUT)
    
def loop():
    while True:
        GPIO.output(led, GPIO.HIGH)
        print("on")
        sleep(2)
        GPIO.output(led, GPIO.LOW)
        print("off")

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()