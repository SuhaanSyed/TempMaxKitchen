import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


buzzer = 17
button = 18
sensor1 = 23
sensor2 = 27
ledPins = [22, 24, 12]



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
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensor1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sensor2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def setColor(r, g, b):
    pwmRed.ChangeDutyCycle(r)
    pwmGreen.ChangeDutyCycle(g)
    pwmBlue.ChangeDutyCycle(b)
def loop():
    while True:
        if GPIO.input(button)==GPIO.LOW:
            setColor(0, 100, 0)
            GPIO.output(buzzer, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(buzzer, GPIO.LOW)
            sleep(1)
            for i in range(2):
                motion = max(GPIO.input(sensor1), GPIO.input(sensor2))
                if motion==GPIO.HIGH:
                    setColor(0, 0, 100)
                    print("motion detected")
                else:
                    print("not detected")
            print("buzzer on")
            sleep(2)
        else:
            GPIO.output(buzzer, GPIO.LOW)
            setColor(0,0,0)
            print("buzzer off")
            sleep(2)

def destroy():
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()



if __name__ == '__main__':
    print("program is starting")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
