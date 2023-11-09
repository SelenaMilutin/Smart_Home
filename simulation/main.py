
import threading
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from console.console import run_console
from components.dus import run_dus
import time



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
        # dht1_settings = settings['RDHT1']
        # run_dht(dht1_settings, threads, stop_event)
        # dht2_settings = settings['RDHT2']
        # run_dht(dht2_settings, threads, stop_event)
        # ds1_setings = settings["DS1"]
        # run_ds(ds1_setings, threads, stop_event)
        run_console(settings, threads, stop_event)
        # dus1_settings = settings["DUS1"]
        # run_dus(dus1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
