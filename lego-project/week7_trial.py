# from buildhat import Motor

# motor_c = Motor('C ')

# motor_c.run_for_seconds(5, speed=50)

from signal import pause
from buildhat import ForceSensor, ColorSensor

button = ForceSensor('C')
cs = ColorSensor('B')

def handle_pressed(force):
	cs.on()
	print(cs.get_color())
	
def handle_released(force):
	cs.off()
	
button.when_pressed = handle_pressed
button.when_released = handle_released
pause()
