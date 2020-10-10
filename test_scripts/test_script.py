from time import sleep

import board

from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

kit.motor1.throttle = 1.0

input("Press Enter")

kit.motor1.throttle = 0.5

input("Press Enter")

kit.motor1.throttle = -0.5

input("Press Enter")

kit.motor1.throttle = 0