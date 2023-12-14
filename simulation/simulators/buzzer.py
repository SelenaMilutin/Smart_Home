
import time
from pynput import keyboard

from server.messenger_sender import send_measurement

def on_press(key, settings):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.space:
        print("Buzzzz")
        send_measurement(1, settings)
    
def on_release(key, settings):
    if key == keyboard.Key.space:
        print("No more buzz")
        send_measurement(0, settings)
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False
    

def run_buzz_simulation(settings, callback, stop_event):
    with keyboard.Listener(on_press=lambda k: on_press(k, settings), on_release=lambda k: on_release(k, settings)) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return