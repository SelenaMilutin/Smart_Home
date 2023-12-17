import RPi.GPIO as GPIO
import time

def custom_callback(callback, settings):
    print(f"Callback wrapper with settings: {settings}")
    callback(settings)

def run_pir_loop(settings, callback, stop_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.IN)

    callback_with_params = lambda: custom_callback(callback = callback, settings=settings)
    
    GPIO.add_event_detect(settings['pin'], GPIO.RISING, callback=callback_with_params)
    # GPIO.add_event_detect(port, GPIO.FALLING, callback=no_motion)

    # if stop_event.is_set():
    #     return