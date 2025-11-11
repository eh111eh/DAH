from buildhat import Motor, MotorPair, ColorSensor
import time


tong = Motor('D')
rotator = Motor('C')
motor = Motor('A')
color = ColorSensor('B')

rotator.run_for_rotations(0.3, speed=5)
