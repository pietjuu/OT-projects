import RPi.GPIO as GPIO
import time

# --- Instellingen ---
RELAY_PIN = 15
ACTIVE_LOW = False
COUNT = 5
INTERVAL = 1.0

AAN = GPIO.LOW if ACTIVE_LOW else GPIO.HIGH
UIT = GPIO.HIGH if ACTIVE_LOW else GPIO.LOW


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=UIT)  # start altijd in UIT-stand

    print(f"test relais{RELAY_PIN} (active_low={ACTIVE_LOW})")
    try:
        for i in range(1, COUNT + 1):
            print(f"[{i}/{COUNT}] Relais ON")
            GPIO.output(RELAY_PIN, AAN)
            time.sleep(INTERVAL)

            print(f"[{i}/{COUNT}] Relais OFF")
            GPIO.output(RELAY_PIN, UIT)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nUser cancelled.")

    finally:
        GPIO.output(RELAY_PIN, UIT)
        GPIO.cleanup()
        print("Relais off, everything is cleaned")


if __name__ == "__main__":
    main()