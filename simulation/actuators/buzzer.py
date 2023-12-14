import time
from pynput import keyboard
from functools import partial

from server.messenger_sender import send_measurement

# def ctrl(letter): return chr(ord(letter.upper())-64)



def on_press_real(port, settings, key):
    if key == keyboard.Key.space:
        # print("jsjs")
        try:
            pitch = 440
            duration = 0.1
            period = 1.0 / pitch
            delay = period / 2
            cycles = int(duration * pitch)
            for i in range(cycles):
                GPIO.output(port, True)
                time.sleep(delay)
                GPIO.output(port, False)
                time.sleep(delay)
            print("Buzzzz")
            send_measurement(1, settings)
        except IOError:
            print("Error")
    
def on_release_real(port, settings, key):
    print(port)
    if key == keyboard.Key.space:
        print("No more buzz")
        send_measurement(0, settings)
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False

        
def run_buzz_legit(settings, stop_event):
    # print("alelelele")
    port = settings['pin']
    import RPi.GPIO as GPI
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)
    with keyboard.Listener(on_press=partial(on_press_real, port, settings), on_release=partial(on_release_real, port, settings)) as listener:
        listener.join()