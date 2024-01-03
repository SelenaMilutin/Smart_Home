import time
from pynput import keyboard
from functools import partial


def run_light_loop(settings, callback, stop_event, publish_event):
    # """
    #     Toggles light based on value of settings.
    #     Settings are updated in component by receiving mqtt message.
    # """

    port = settings['pin']
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)
    while True:
        if settings['on']:
            GPIO.output(settings['pin'], GPIO.HIGH)
            callback(1, settings, publish_event)
        else: 
            GPIO.output(settings['pin'], GPIO.LOW)
            callback(0, settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(1)  
