from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

print("--- CALIBRATION MODE ---")
print("Putting all arm servos (0-11) to 90 degrees (center)...")

try:
    for channel in range(12):
        kit.servo[channel].angle = 90
        time.sleep(0.1) 

    print("\nAll motors are locked at 90 degrees.")
    print("DO NOT close the program or unplug power!")
    print("Now screw the arms on straight down.")
    
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nCalibration stopped.")