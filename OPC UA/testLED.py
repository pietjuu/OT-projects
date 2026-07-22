import RPi.GPIO as GPIO
import time

LED_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.HIGH)  # aan
time.sleep(1)
GPIO.output(LED_PIN, GPIO.LOW)   # uit
GPIO.cleanup()