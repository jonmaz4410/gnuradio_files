import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(40, GPIO.OUT)

try: 
	GPIO.output(40, GPIO.HIGH)
	print("GPIO pin 40 activated")
	
	time.sleep(60)
	
	GPIO.output(40, GPIO.LOW)
	print("GPIO pin 40 is off")
	
finally:
	GPIO.cleanup()
	
