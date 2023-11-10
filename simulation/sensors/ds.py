import RPi.GPIO as GPIO
import time

def run_ds_loop(port, callback, stop_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(port, GPIO.RISING, callback =
        callback, bouncetime = 100)
    # if stop_event.is_set():
    #     return

    
    # while True:
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #     GPIO.add_event_detect(port, GPIO.RISING, callback =
    #     callback, bouncetime = 100)
    #     if stop_event.is_set():
    #         break
          
	    