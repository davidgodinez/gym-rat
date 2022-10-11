# Accelerometer - By: David.Godinez - Mon Oct 10 2022

import time
import lsm9ds1
from machine import Pin, I2C
from board import LED


led_red = LED(1)
led_green = LED(2)
led_blue = LED(3)
led_yellow = LED(4)
bus = I2C(1, scl=Pin(15), sda=Pin(14))
lsm = lsm9ds1.LSM9DS1(bus)

while (True):
    if lsm.read_gyro()[1] >= 0:
        print('up')
        #led_green.on()
        #time.sleep_ms(100)
        #led_green.off()
    elif lsm.read_gyro()[1] <= 0:
        print('down')
        #led_yellow.on()
        #time.sleep_ms(100)
        #led_yellow.off()
    #for g,a in lsm.iter_accel_gyro(): print(g,a)    # using fifo
    #print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_accel()))
    #print('Magnetometer:  x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_magnet()))
    #print('Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_gyro()))
    print('Gyroscope: y:{:8.3f}'.format(lsm.read_gyro()[1]))
    print("")
    time.sleep_ms(500)
