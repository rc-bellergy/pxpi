# sudo apt install python3-smbus
# pip install mpu6050-raspberrypi

from mpu6050 import mpu6050
from time import sleep
from sys import exit

sensor = mpu6050(0x68)

try:
    while True:
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temp = sensor.get_temp()

        print("Accelerometer data")
        print("x: " + str(accel_data['x']))
        print("y: " + str(accel_data['y']))
        print("z: " + str(accel_data['z']))

        print("Gyroscope data")
        print("x: " + str(gyro_data['x']))
        print("y: " + str(gyro_data['y']))
        print("z: " + str(gyro_data['z']))

        print("Temp: " + str(temp) + " C")
        sleep(0.5)
except KeyboardInterrupt:
    exit()
