# import keyboard
import threading
import time

from pynput import keyboard

from server.messenger_sender import send_measurement

def on_press(key, settings):
    # print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.shift_l:
        print("Light is set to ON")
        print(settings['on'])
        settings['on'] = True
        print(settings['on'])
        send_measurement(1, settings)
    
def on_release(key, settings):
    if key == keyboard.Key.backspace:
        print("Light is set to OFF")
        settings['on'] = False
        send_measurement(0, settings)
    if key == keyboard.Key.esc:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False

def loop_function(settings, stop_event):
    while True:
        if settings['on']: send_measurement(1, settings)
        if not settings['on']: send_measurement(0, settings)
        if stop_event.is_set():
            keyboard.Listener.stop
            return
        time.sleep(1)


def run_light_simulator(settings, callback, stop_event):
    loop_thread = threading.Thread(target=loop_function, args=(settings, stop_event))
    loop_thread.start()
    with keyboard.Listener(on_press=lambda k: on_press(k, settings), on_release=lambda k: on_release(k, settings)) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return
    