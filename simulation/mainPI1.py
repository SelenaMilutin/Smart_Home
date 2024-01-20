
import threading
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
from components.light import run_light
from components.pir import run_pir
import time
from components.buzzer import run_buzzer



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
        # dus1_settings = settings["DUS1"]
        # run_dus(dus1_settings, threads, stop_event)
        dms_settings = settings["DMS"]
        run_dms(dms_settings, threads, stop_event)
        # light_settings = settings["DL"]
        # run_light(light_settings, threads, stop_event)
        # rpir1_setings = settings["RPIR1"]
        # run_pir(rpir1_setings, threads, stop_event, "room")
        # rpir2_setings = settings["RPIR2"]
        # run_pir(rpir2_setings, threads, stop_event, "room")
        # dpir1_setings = settings["DPIR1"]
        # run_pir(dpir1_setings, threads, stop_event, "door")
        # buzzer_setings = settings["DB"]
        # run_buzzer(buzzer_setings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
