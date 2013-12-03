#!/usr/bin/python
print "Setting GPIO pin 17 to FALSE for .5 seconds"
import time
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)
time.sleep(0.5)
GPIO.output(17, True)
GPIO.cleanup()
