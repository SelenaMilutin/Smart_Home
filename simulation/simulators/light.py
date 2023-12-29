# import keyboard
import threading
import time

from pynput import keyboard


def on_press(key, settings, publish_event, callback):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.shift_l:
        print("Light is set to ON")
        print(settings['on'])
        settings['on'] = True
        print(settings['on'])
        callback(1, settings, publish_event)
    
def on_release(key, settings, publish_event, callback):
    if key == keyboard.Key.backspace:
        print("Light is set to OFF")
        settings['on'] = False
        callback(0, settings, publish_event)
    if key == keyboard.Key.esc:
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


def run_light_simulator(settings, callback, stop_event, publish_event):
    loop_thread = threading.Thread(target=loop_function, args=(settings, stop_event, publish_event, callback))
    loop_thread.start()
    with keyboard.Listener(on_press=lambda k: on_press(k, settings, publish_event, callback), on_release=lambda k: on_release(k, settings, publish_event, callback)) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return
    