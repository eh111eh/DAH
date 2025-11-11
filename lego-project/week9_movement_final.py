from buildhat import Motor, ColorSensor
import time

drive = Motor('A')       # forward movement motor
color = ColorSensor('B') # colour sensor
rotator = Motor('C')     # rotates the arm to drop green block
tong = Motor('D')        # grabs/releases block

def detect_block():
    """
    Returns True if reflection indicates a block is in front of sensor.
    """
    return color.get_reflected_light() > 50

def detect_color():
    """
    Try to detect color 5 times and return the most common result.
    """
    samples = []
    for i in range(5):
        samples.append(color.get_color())
        time.sleep(0.05)

    # Pick the most frequently detected colour
    most_common = max(set(samples), key=samples.count)
    return most_common

def pick_and_place_green():
    """
    Performs the movement sequence to place block in the back basket.
    """
    # rotate arm down to pick
    rotator.run_for_rotations(-0.5, speed=5)

    # close tong
    tong.run_for_rotations(-0.6, speed=5)

    # lift slightly
    rotator.run_for_rotations(0.2, speed=5)

    # drive backward slightly to position at basket
    drive.run_for_rotations(0.5, speed=3)

    # lower tong at basket
    rotator.run_for_rotations(-0.6, speed=5)

    # open tong to release block
    tong.run_for_rotations(0.5)

# MAIN LOOP
print("Starting robot...")

while True:

    # Move forward continuously
    drive.start(speed=10)

    # Check if a block appears
    if detect_block():
        drive.stop()

        # Get reliable color (5-sample)
        detected = detect_color()
        print("Detected colour:", detected)

        if detected == "green":
            print("Green block found — picking up.")
            pick_and_place_green()

            # After placing, go forward again
            drive.run_for_rotations(0.3, speed=20)

        else:
            print("Not green — ignoring block.")
            # Move forward slightly to avoid double-detection
            drive.run_for_rotations(0.3, speed=20)
