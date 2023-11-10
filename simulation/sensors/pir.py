import RPi.GPIO as GPIO
import time

def run_pir_loop(port, callback, stop_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.IN)
    
    GPIO.add_event_detect(port, GPIO.RISING, callback=callback)
    # GPIO.add_event_detect(port, GPIO.FALLING, callback=no_motion)

    # if stop_event.is_set():
    #     return