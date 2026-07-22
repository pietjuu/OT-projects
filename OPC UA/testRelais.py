"""
Testscript voor de Keyes 8-kanaals relaismodule op de Raspberry Pi.

Sluit IN1 van de relaismodule aan op de GPIO-pin hieronder (RELAY_PIN),
VCC op 5V en GND op GND.

Dit board is meestal ACTIVE-LOW: GPIO.LOW = relais AAN (klik),
GPIO.HIGH = relais UIT (klik). Als het bij jou omgekeerd werkt,
zet dan ACTIVE_LOW = False.
"""

import RPi.GPIO as GPIO
import time

# --- Instellingen ---
RELAY_PIN = 17       # GPIO-nummer (BCM) waarop IN1 is aangesloten
ACTIVE_LOW = True     # True = board schakelt AAN bij GPIO.LOW (meest gangbaar)
AANTAL_KEER = 5       # hoeveel keer laten klikken
INTERVAL = 1.0         # seconden tussen aan/uit

AAN = GPIO.LOW if ACTIVE_LOW else GPIO.HIGH
UIT = GPIO.HIGH if ACTIVE_LOW else GPIO.LOW


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=UIT)  # start altijd in UIT-stand

    print(f"Relais testen op GPIO{RELAY_PIN} (active_low={ACTIVE_LOW})")
    try:
        for i in range(1, AANTAL_KEER + 1):
            print(f"[{i}/{AANTAL_KEER}] Relais AAN")
            GPIO.output(RELAY_PIN, AAN)
            time.sleep(INTERVAL)

            print(f"[{i}/{AANTAL_KEER}] Relais UIT")
            GPIO.output(RELAY_PIN, UIT)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nOnderbroken door gebruiker.")

    finally:
        GPIO.output(RELAY_PIN, UIT)  # veilig afsluiten: relais uit
        GPIO.cleanup()
        print("GPIO opgeruimd, relais staat UIT.")


if __name__ == "__main__":
    main()