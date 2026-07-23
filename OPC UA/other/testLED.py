import RPi.GPIO as GPIO
import time

BUTTON_PIN = 16
LED_PIN = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Druk op de knop... (Ctrl+C om te stoppen)")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("Knop ingedrukt, LED aan")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()