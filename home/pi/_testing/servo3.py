#!/usr/bin/python3

# Install:
# sudo apt-get update && sudo apt-get install python3-pigpio

# http://abyz.me.uk/rpi/pigpio/

# Strat server demon:
# sudo pigpiod 

import pigpio
from time import sleep

PIN=24            ## Gservo at GPIO24 PIN
pwm = pigpio.pi()   # accesses the local Pi's GPIO
pwm.set_mode(PIN, pigpio.OUTPUT) # Set GPIO24 as output
pwm.set_PWM_frequency(PIN, 50)

pwm.set_servo_pulsewidth(PIN, 0) # Starts (500-2500) or stops (0) servo pulses on the GPIO

try:
     while True:
          pwm.set_servo_pulsewidth(PIN, 1000)
          print("min:1000")
          sleep(1)

          pwm.set_servo_pulsewidth(PIN, 1500)
          print("mid:1500")
          sleep(1)

          pwm.set_servo_pulsewidth(PIN, 1000)
          print("max:2000")
          sleep(1)

except KeyboardInterrupt:
     pwm.set_PWM_dutycycle(PIN, 0)
     pwm.set_PWM_frequency(PIN, 0)
     exit()