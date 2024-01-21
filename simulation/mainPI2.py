
import threading
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
from components.light import run_light
from components.pir import run_pir
import time
from components.gyro import run_gyro
from components.lcd import run_LCDdisplay
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
        # buzzer_setings = settings["DB"]
        # run_buzzer(buzzer_setings, threads, stop_event)

        button = settings["DS2"]
        run_ds(button, threads, stop_event)

        dus1_settings = settings["DUS2"]
        run_dus(dus1_settings, threads, stop_event)
        
        dpir1_setings = settings["DPIR2"]
        run_pir(dpir1_setings, threads, stop_event, "door")
        
        rpir2_setings = settings["RPIR3"]
        run_pir(rpir2_setings, threads, stop_event, "room")
        
        gyro_setings = settings["GSG"]
        run_gyro(gyro_setings, threads, stop_event)

        garage_dht_settings = settings["GDHT"]
        run_dht(garage_dht_settings, threads, stop_event)


        garage_lcd_settings = settings["GLCD"]
        run_LCDdisplay(garage_lcd_settings, threads, stop_event)  

        room_dht_settings = settings["RDHT3"]
        run_dht(room_dht_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
