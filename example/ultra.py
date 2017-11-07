import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
trig = 11
echo = 13
gpio.setup(trig, gpio.OUT,initial=gpio.LOW)
gpio.setup(echo, gpio.IN)
try :
        while True :
                gpio.output(trig,False)
                time.sleep(0.5)
                gpio.output(trig, True)
                time.sleep(0.000001)
                gpio.output(trig, False)
                print ('1')
                while True :
                        print ('2222')
                        if gpio.input(echo) == 0 :
                                print ('2')
                                pass
                        else :
                                start_time = time.time()
                                print ('start_time = '+start_time)
                                break
                while True :
                        if gpio.input(echo) == 1 :
                                print ('3')
                                pass
                        else :
                                end_time = time.time()
                                print ('end_time ='+end_time)
                                break
                distance = (end_time - start_time) * 17000
                print (' Dist = '+ distance)
        
        print ('1111111')
except :
        gpio.cleanup()
        print (' ')
        print (' == Good Bye == ')

