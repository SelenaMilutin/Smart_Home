import RPi.GPIO as GPIO
import time

def custom_callback(callback, settings, publish_event):
    print(f"Callback wrapper with settings: {settings}")
    callback(settings, publish_event)

def run_ds_loop(settings, callback, stop_event, publish_event):
    port = settings['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    callback_with_params = lambda channel: custom_callback(callback = callback, settings=settings, publish_event=publish_event)

    GPIO.add_event_detect(port, GPIO.RISING, callback =
        callback_with_params, bouncetime = 100)
    
    
    # while True:
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #     GPIO.add_event_detect(port, GPIO.RISING, callback =
    #     callback, bouncetime = 100)
    #     if stop_event.is_set():
    #         break
          
	    