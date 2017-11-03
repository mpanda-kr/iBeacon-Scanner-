import RPi.GPIO as GPIO
import time

counter = 0
BuzzerPin = 18
Moction = 40
GPIO.setmode(GPIO.BOARD)

GPIO.setup(Moction, GPIO.IN)
GPIO.setup(BuzzerPin, GPIO.OUT)
GPIO.output(BuzzerPin, GPIO.LOW)

def motionSensor(channel) :
    print("come in!!")
    if GPIO.input(channel) == 1: # detecting
        global counter
        counter += 1
        GPIO.output(BuzzerPin, GPIO.HIGH)
        print("Motion detected! [{0}]".format(counter))
        GPIO.output(BuzzerPin, GPIO.LOW)

GPIO.add_event_detect(Moction, GPIO.BOTH, callback=motionSensor, bouncetime=150)

#print("GPIO VERSION={0}".format(GPIO.VERSION))

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nInterrupted!")

finally:
    GPIO.cleanup()
