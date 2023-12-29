
import time
from pynput import keyboard


def on_press(key, settings, callback, publish_event):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.space:
        print("Buzzzz")
        callback(1, settings, publish_event)
    
def on_release(key, settings, callback, publish_event):
    if key == keyboard.Key.space:
        print("No more buzz")
        callback(0, settings, publish_event)
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False
    

def run_buzz_simulation(settings, callback, stop_event, publish_event):
    with keyboard.Listener(on_press=lambda k: on_press(k, settings, callback, publish_event), on_release=lambda k: on_release(k, settings, callback, publish_event)) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return