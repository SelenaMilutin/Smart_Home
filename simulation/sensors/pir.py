import RPi.GPIO as GPIO
import time

def custom_callback(callback, settings, publish_event):
    print(f"Callback wrapper with settings: {settings}")
    callback(settings, publish_event)

def run_pir_loop(settings, callback, stop_event, publish_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.IN)

    isDPIR1 = True if settings.get("isDoor") != None and settings.get("isDoor") else False
    callback_with_params = lambda channel: custom_callback(callback = callback, settings=settings, publish_event=publish_event, isDPIR1=isDPIR1, verbose=True)
    
    GPIO.add_event_detect(settings['pin'], GPIO.RISING, callback=callback_with_params)
    # GPIO.add_event_detect(port, GPIO.FALLING, callback=no_motion)

    # if stop_event.is_set():
    #     return