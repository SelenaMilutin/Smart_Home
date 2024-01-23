
import threading
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
import time
from simulation.components.bir import run_bir

from simulation.components.display4D7S import run_4D7Sdisplay
from simulation.components.rgb import run_rgb


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # rpir1_setings = settings["RPIR4"]
        # run_pir(rpir1_setings, threads, stop_event, "room")
        # dht1_settings = settings['RDHT4']
        # run_dht(dht1_settings, threads, stop_event)
        # buzzer_setings = settings["BB"]
        # run_buzzer(buzzer_setings, threads, stop_event)
        # display4D7s_settings = settings["B4SD"]
        # run_4D7Sdisplay(display4D7s_settings, threads, stop_event)
        # bir_settings = settings["BIR"]
        # run_bir(bir_settings, threads, stop_event)
        rgb_settings = settings["BRGB"]
        run_rgb(rgb_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
