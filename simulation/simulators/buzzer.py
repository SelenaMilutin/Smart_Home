
import time
from pynput import keyboard
import threading


def loop_function(settings, stop_event, publish_event, callback):
    while True:
        if settings['on']: callback(1, settings, publish_event)
        if not settings['on']: callback(0, settings, publish_event)
        if stop_event.is_set():
            return
        time.sleep(1)    

def run_buzz_simulation(settings, callback, stop_event, publish_event):
    loop_thread = threading.Thread(target=loop_function, args=(settings, stop_event, publish_event, callback))
    loop_thread.start()
    if stop_event.is_set():
        return