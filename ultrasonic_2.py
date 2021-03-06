#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_2.py
# Measure distance using an ultrasonic module
# in a loop.
#
# Ultrasonic related posts:
# http://www.raspberrypi-spy.co.uk/tag/ultrasonic/
#
# Author : Matt Hawkins
# Date   : 16/10/2016
# -----------------------

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import print_function
import time
import RPi.GPIO as GPIO
import datetime
import sqlite3
import threading
import ultra_scan_gateway_to_server

# -----------------------
# Define some functions
# -----------------------
def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.

  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
BuzzerPin = 12
# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)

print("Ultrasonic Measurement")
print("Speed of sound is",speedSound/100,"m/s at ",temperature,"deg")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

GPIO.setup(BuzzerPin, GPIO.OUT)
GPIO.output(BuzzerPin, GPIO.LOW)

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.

#sqlite3 config

con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor = con.cursor()

before_distance = 0
now_distance = 0

# BuzzerPin = 16
# GPIO.setup(BuzzerPin, GPIO.OUT)
# GPIO.output(BuzzerPin, GPIO.HIGH)
  
try:
  while True:
    distance = measure_average()
    now = datetime.datetime.now()
    print("====================================")
    print("Distance : {0:5.1f}".format(distance))
    print("Time : " + str(datetime.datetime.now()))
    print("====================================")
   
    diff = before_distance - distance
    before_distance = distance

    if diff > 60:
      GPIO.output(BuzzerPin, GPIO.HIGH)
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  ",diff )      
      cursor.execute("insert into test_ultra_log (createtime,distance,diff) values ('"+str(now)+"',"+ str(distance)+","+str(diff)+")")
      con.commit()
      ultra_scan_gateway_to_server.ultra_scan()
      GPIO.output(BuzzerPin, GPIO.LOW)

      
    else:
      cursor.execute("insert into test_ultra_log (createtime,distance) values ('"+str(now)+"',"+ str(distance)+")")
      con.commit()
      
    # time.sleep(0.3)

finally:
  GPIO.cleanup()
  con.close()
