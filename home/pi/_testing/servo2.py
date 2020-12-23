from gpiozero import Servo
from time import sleep
 
myGPIO=24
 
myCorrection=0
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)
 
while True:
     for value in range(0,10):
          value2=(float(value)-10)/10
          servo.value=value2
          print(value2)
          sleep(2)