import RPi.GPIO as GPIO
import time

ledPin = 17
sensorPin = 18



def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(sensorPin, GPIO.IN)
    
def loop():
    while True:
        if GPIO.input(sensorPin) == GPIO.HIGH:
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(1)
            print('led turned on')
        else:
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(1)
            print('led turned off')
def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    print("program is starting")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()