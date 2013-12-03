#!/usr/bin/python
print "Content-Type: text/plain;charset=utf-8"
import time
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)
time.sleep(15)
GPIO.output(17, True)
GPIO.cleanup()
