
import time
from pynput import keyboard

def on_press(key):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.space:
        print("Buzzzz")
    
def on_release(key):
    if key == keyboard.Key.space:
        print("No more buzz")
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False
    

def run_buzz_simulation(callback, stop_event):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return