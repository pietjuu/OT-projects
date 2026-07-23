"""
test_proces.py

Doorloopt automatisch een aantal scenario's om de Proces-klasse te testen:
1. Klep open -> niveau moet stijgen
2. Pomp aan -> niveau moet dalen
3. Verlaagde alarmdrempel -> alarm_hoog moet triggeren, LED aan
4. Terug naar veilige staat

Gebruik dit los van proces.py's eigen testblok, om sneller specifieke
scenario's te controleren zonder telkens in de REPL te typen.
"""

import time
import proces
from OTSimulation import Proces


def print_status(label, p):
    print(f"\n--- {label} ---")
    print(p.get_status())


def main():
    p = Proces()

    try:
        print_status("Start", p)

        # --- Scenario 1: klep open, niveau moet stijgen ---
        print("\n>> Klep naar 90 graden (open)...")
        p.set_klep_hoek(90)
        time.sleep(5)
        print_status("Na 5s met klep open", p)

        # --- Scenario 2: pomp aan, niveau moet dalen ---
        print("\n>> Klep dicht, pomp aan...")
        p.set_klep_hoek(0)
        p.set_pomp(True)
        time.sleep(5)
        print_status("Na 5s met pomp aan", p)

        p.set_pomp(False)

        # --- Scenario 3: alarmdrempel verlagen om alarm_hoog te forceren ---
        print("\n>> Testdrempel instellen om alarm_hoog te forceren...")
        huidig_niveau = p.get_niveau()
        proces.ALARM_HOOG = huidig_niveau + 2  # net iets boven huidig niveau
        p.set_klep_hoek(90)
        time.sleep(6)
        print_status("Na verlaagde drempel + klep open", p)

        if p.get_status()["alarm_hoog"]:
            print(">> alarm_hoog is getriggerd, LED zou moeten branden.")
        else:
            print(">> alarm_hoog nog niet getriggerd, wacht iets langer of verlaag de drempel verder.")

        # --- Terug naar veilige staat ---
        p.set_klep_hoek(0)
        p.set_pomp(False)
        print_status("Eind (veilige staat)", p)

    finally:
        p.stop()
        print("\nProces netjes afgesloten.")


if __name__ == "__main__":
    main()