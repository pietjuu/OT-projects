import RPi.GPIO as GPIO
import time

# Variables
RELAY_PIN = 15
ACTIVE_LOW = False
COUNT = 5
INTERVAL = 1.0

ON = GPIO.LOW if ACTIVE_LOW else GPIO.HIGH
OFF = GPIO.HIGH if ACTIVE_LOW else GPIO.LOW
GPIO.setwarnings(False)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=OFF)  # start altijd in UIT-stand

    print(f"test relais{RELAY_PIN} (active_low={ACTIVE_LOW})")
    try:
        for i in range(1, COUNT + 1):
            print(f"[{i}/{COUNT}] Relais ON")
            GPIO.output(RELAY_PIN, ON)
            time.sleep(INTERVAL)

            print(f"[{i}/{COUNT}] Relais OFF")
            GPIO.output(RELAY_PIN, OFF)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nUser cancelled.")

    finally:
        GPIO.output(RELAY_PIN, OFF)
        GPIO.cleanup()
        print("Relais off, everything is cleaned")


if __name__ == "__main__":
    main()