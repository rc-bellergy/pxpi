# pip3 install RPi.GPIO

import RPi.GPIO as GPIO         ## pip3 install RPi.GPIO
import time
 
GPIO.setmode(GPIO.BCM)          ## Use BOARD pin numbering.
GPIO.setup(23, GPIO.OUT)        ## GPIO23

pwm=GPIO.PWM(24,80)             ## PWM Frequency
pwm.start(5)
 
angle1=0
duty1= float(angle1)/10 + 2.5               ## Angle To Duty cycle  Conversion
print("duty1",duty1)
 
angle2=90
duty2= float(angle2)/10 + 2.5
print("duty2",duty2)
 
ck=0
while ck<=5:
     pwm.ChangeDutyCycle(duty1)
     time.sleep(0.8)
     pwm.ChangeDutyCycle(duty2)
     time.sleep(0.8)
     ck=ck+1
time.sleep(1)
GPIO.cleanup()