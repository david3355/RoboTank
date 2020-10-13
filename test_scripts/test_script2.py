from time import sleep

import board

from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

print("Running on full speed")
kit.motor2.throttle = 1.0
kit.motor1.throttle = -1.0

input("Press Enter")


print("Stop")
kit.motor1.throttle = 0
kit.motor2.throttle = 0
