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

x = range(700, 1700, 3)

try:
    while True:
        for n in x:
            pwm.set_servo_pulsewidth(PIN, n)
            print(n)
            sleep(0.01)

except KeyboardInterrupt:
     pwm.set_PWM_dutycycle(PIN, 0)
     pwm.set_PWM_frequency(PIN, 0)
     print("servo off")
     exit()
