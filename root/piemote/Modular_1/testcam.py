import time
import RPi.GPIO as GPIO
 
# Use GPIO numbering
GPIO.setmode(GPIO.BCM)
 
# Set GPIO for camera LED
# Use 5 for Model A/B and 32 for Model B+
CAMLED = 32 
 
# Set GPIO to output
GPIO.setup(CAMLED, GPIO.OUT, initial=False) 
 
# Five iterations with half a second
# between on and off
for i in range(2):
 GPIO.output(CAMLED,True) # On
 time.sleep(0.5)
 print ("ON") 
 GPIO.output(CAMLED,False) # Off
 time.sleep(0.5)
 print ("PFF")
