import time
import threading
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

# Hardware settings
RELAY_PIN = 17        # GPIO (BCM) voor de pomp-relais
LED_PIN = 26           # GPIO (BCM) voor de alarm-LED
BUTTON_PIN = 16        # GPIO (BCM) voor de noodstop-knop
SERVO_CHANNEL = 0      # kanaal op de PCA9685 voor de klep-servo
RELAY_ACTIVE_LOW = True  # True = relais AAN bij GPIO.LOW (meest gangbaar)

# Process Variables
LEVEL_START = 50.0     # % vulling bij opstarten
LEVEL_ASCENT_RATE = 0.5   # % per seconde wanneer klep open staat en pomp uit
LEVEL_DECENT_RATE = 1.0    # % per seconde wanneer pomp aan staat
ALARM_HIGH = 80.0
ALARM_LOW = 10.0


class Proces:
    def __init__(self):
        # --- GPIO init ---
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        relay_uit = GPIO.HIGH if RELAY_ACTIVE_LOW else GPIO.LOW
        GPIO.setup(RELAY_PIN, GPIO.OUT, initial=relay_uit)

        # --- Servo init ---
        self.kit = ServoKit(channels=16)

        # --- Interne staat ---
        self._klep_hoek = 0.0          # 0-180 graden
        self._pomp_aan = False
        self._alarm_hoog = False
        self._alarm_laag = False
        self._niveau = LEVEL_START
        self._noodstop = False

        self._lock = threading.Lock()
        self._running = True

        # Servo naar startpositie (klep dicht)
        self.set_klep_hoek(0)

        # Achtergrondthread: simuleert het tankniveau en leest de noodstopknop
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    # ---------- Klep (servo) ----------
    def set_klep_hoek(self, hoek: float):
        hoek = max(0.0, min(180.0, hoek))
        with self._lock:
            self._klep_hoek = hoek
            self.kit.servo[SERVO_CHANNEL].angle = hoek

    def get_klep_hoek(self) -> float:
        with self._lock:
            return self._klep_hoek

    # ---------- Pomp (relais) ----------
    def set_pomp(self, aan: bool):
        with self._lock:
            self._pomp_aan = aan
            waarde = GPIO.LOW if (aan == RELAY_ACTIVE_LOW) else GPIO.HIGH
            GPIO.output(RELAY_PIN, waarde)

    def get_pomp(self) -> bool:
        with self._lock:
            return self._pomp_aan

    # ---------- Alarm (LED) ----------
    def _set_led(self, aan: bool):
        GPIO.output(LED_PIN, GPIO.HIGH if aan else GPIO.LOW)

    # ---------- Noodstop (drukknop) ----------
    def get_noodstop(self) -> bool:
        with self._lock:
            return self._noodstop

    # ---------- Tankniveau ----------
    def get_niveau(self) -> float:
        with self._lock:
            return self._niveau

    def get_status(self) -> dict:
        """Geeft een snapshot van de volledige processtatus terug."""
        with self._lock:
            return {
                "klep_hoek": self._klep_hoek,
                "pomp_aan": self._pomp_aan,
                "niveau": round(self._niveau, 1),
                "alarm_hoog": self._alarm_hoog,
                "alarm_laag": self._alarm_laag,
                "noodstop": self._noodstop,
            }

    # ---------- Achtergrondlus: simulatie + sensoren ----------
    def _loop(self):
        vorige_tijd = time.time()
        while self._running:
            time.sleep(0.2)
            nu = time.time()
            dt = nu - vorige_tijd
            vorige_tijd = nu

            with self._lock:
                # Noodstopknop uitlezen
                self._noodstop = GPIO.input(BUTTON_PIN) == GPIO.HIGH

                # Simuleer niveauverandering
                if self._pomp_aan:
                    self._niveau -= LEVEL_DECENT_RATE * dt
                elif self._klep_hoek > 10:
                    self._niveau += LEVEL_ASCENT_RATE * dt

                self._niveau = max(0.0, min(100.0, self._niveau))

                # Alarmlogica
                self._alarm_hoog = self._niveau >= ALARM_HIGH
                self._alarm_laag = self._niveau <= ALARM_LOW
                alarm_actief = self._alarm_hoog or self._alarm_laag or self._noodstop

            self._set_led(alarm_actief)

            # Veiligheid: noodstop -> pomp uit en klep dicht
            if self._noodstop:
                self.set_pomp(False)
                self.set_klep_hoek(0)

    def stop(self):
        self._running = False
        self._thread.join(timeout=1)
        self.set_pomp(False)
        self.set_klep_hoek(0)
        self.kit.servo[SERVO_CHANNEL].angle = None  # servo loslaten
        GPIO.cleanup()


# --- Simpele test wanneer je dit bestand direct uitvoert ---
if __name__ == "__main__":
    proces = Proces()
    try:
        print("Proces gestart. Ctrl+C om te stoppen.")
        while True:
            print(proces.get_status())
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        proces.stop()
        print("Proces netjes afgesloten.")