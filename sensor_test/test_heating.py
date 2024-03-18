import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(40, GPIO.OUT)

while True:
    GPIO.output(40,GPIO.HIGH)
