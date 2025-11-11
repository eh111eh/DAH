from buildhat import Motor, MotorPair, ColorSensor
import time


tong = Motor('D')
rotator = Motor('C')
motor = Motor('A')
color = ColorSensor('B')

while color != 'green':
	# motor.run_for_rotations(1, speedl=10, speedr=10)
	color = color.get_color()
	
	if color == 'green':
		# motor.stop()
		rotator.run_for_rotations(-0.5, speed=5)
		tong.run_for_rotations(-0.6, speed=5)
		rotator.run_for_rotations(0.2, speed=5)
		motor.run_for_rotations(0.5, speed=3)
		rotator.run_for_rotations(-0.6, speed=5)
		tong.run_for_rotations(0.5)
