
import time
from pynput import keyboard
import threading


def on_press(key, settings, callback, publish_event):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.space:
        settings['on'] = True
        print("Buzzzz")
        callback(1, settings, publish_event)
    
def on_release(key, settings, callback, publish_event):
    if key == keyboard.Key.space:
        settings['on'] = False
        print("No more buzz")
        callback(0, settings, publish_event)
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False

def loop_function(settings, stop_event, publish_event, callback):
    while True:
        if settings['on']: callback(1, settings, publish_event)
        if not settings['on']: callback(0, settings, publish_event)
        if stop_event.is_set():
            keyboard.Listener.stop
            return
        time.sleep(1)    

def run_buzz_simulation(settings, callback, stop_event, publish_event):
    loop_thread = threading.Thread(target=loop_function, args=(settings, stop_event, publish_event, callback))
    loop_thread.start()
    with keyboard.Listener(on_press=lambda k: on_press(k, settings, callback, publish_event), on_release=lambda k: on_release(k, settings, callback, publish_event)) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return