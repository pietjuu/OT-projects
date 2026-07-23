import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
servo_channels = [0, 1, 2, 3]  # active channels

try:
    for channel in servo_channels:
        print(f"Kanaal {channel}: naar 0 graden")
        kit.servo[channel].angle = 0
        time.sleep(1)

        print(f"Kanaal {channel}: naar 90 graden")
        kit.servo[channel].angle = 90
        time.sleep(1)

        print(f"Kanaal {channel}: naar 180 graden")
        kit.servo[channel].angle = 180
        time.sleep(1)

finally:
    # cleanup
    for channel in servo_channels:
        kit.servo[channel].angle = None