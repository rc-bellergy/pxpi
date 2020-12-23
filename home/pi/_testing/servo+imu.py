#!/usr/bin/python3

# Install:
# sudo apt-get update && sudo apt-get install python3-pigpio
# sudo apt install python3-smbus
# pip install mpu6050-raspberrypi (lib of the IMU chip)

# http://abyz.me.uk/rpi/pigpio/

# Strat server demon:
# sudo pigpiod 

from mpu6050 import mpu6050
import pigpio
from time import sleep

# Servo
PIN=24            ## Gservo at GPIO24 PIN
servo = pigpio.pi()   # accesses the local Pi's GPIO
servo.set_mode(PIN, pigpio.OUTPUT) # Set GPIO24 as output
servo.set_PWM_frequency(PIN, 50)
servo.set_servo_pulsewidth(PIN, 0) # Starts (500-2500) or stops (0) servo pulses on the GPIO

# IMU
imu = mpu6050(0x68)

def deg_to_pulse(deg):
    return int(deg * 11.11 + 700)

def imu_to_deg(imu):
    return int(imu * 9)

p1 = 0 # 0 deg
p3 = 90 # 90 deg

target = 0 # keep the camera 0 deg

servo.set_servo_pulsewidth(PIN, 700)
sleep(2)

try:
     while True:

        accel = imu.get_accel_data()
        rotate = target - imu_to_deg(accel['y'])
        if rotate < -15:
            rotate = -15
        if rotate > 90:
            rotate = 90
        print(rotate, deg_to_pulse(rotate))
        servo.set_servo_pulsewidth(PIN, deg_to_pulse(rotate))
        sleep(0.5)

except KeyboardInterrupt:
     servo.set_PWM_dutycycle(PIN, 0)
     servo.set_PWM_frequency(PIN, 0)
     print("servo off")
     exit()
