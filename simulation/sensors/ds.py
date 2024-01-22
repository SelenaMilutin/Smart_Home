import RPi.GPIO as GPIO
import time
import threading

from simulation.alarm.alarm import activate_alarm


def custom_callback(callback, settings, publish_event, threads, channel, stop_event):
    print(f"Callback wrapper with settings: {settings}")
    callback(settings, publish_event)
    rising_thread = threading.Thread(target=run_ds_rising, args=(settings, threads, callback, publish_event, stop_event))
    rising_thread.start()
    threads.append(rising_thread)

    # start_time = time.time()
    # while GPIO.input(channel) == 0: # Wait for the button up
    #     pass
    # buttonTime = time.time() - start_time    # How long was the button down?
    # if buttonTime >= 5:
    #     pass

def run_ds_loop(settings, threads, callback, stop_event, publish_event):
    port = settings['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    callback_with_params = lambda channel: custom_callback(callback = callback, settings=settings, publish_event=publish_event, threads=threads, channel=channel, stop_event=stop_event)

    GPIO.add_event_detect(port, GPIO.FALLING, callback =
        callback_with_params, bouncetime = 100)
    
    GPIO.cleanup()
    # while True:
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #     GPIO.add_event_detect(port, GPIO.RISING, callback =
    #     callback, bouncetime = 100)
    #     if stop_event.is_set():
    #         break
          

def button_pressed(event):
    print("BUTTON PRESS DETECTED")

def run_ds_rising(settings, threads, callback, publish_event, stop_event):
    counter = 0
    alarm_activated = False
    while True:
        is_pressed = GPIO.input(settings["pin"])
        print(is_pressed)
        if not is_pressed:
            if alarm_activated:
                activate_alarm("deactivate", settings["simulated"], settings["name"], settings["runs_on"])
            stop_event.set()
        if counter >= 5:
            alarm_activated = True
            activate_alarm("activate", settings["simulated"], settings["name"], settings["runs_on"])

        counter += 1
        time.sleep(1)
