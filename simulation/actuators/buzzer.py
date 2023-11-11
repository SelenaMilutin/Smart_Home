import time
from pynput import keyboard
from functools import partial

# def ctrl(letter): return chr(ord(letter.upper())-64)



def on_press_real(port, key):
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
        except IOError:
            print("Error")
    
def on_release_real(port, key):
    print(port)
    if key == keyboard.Key.space:
        print("No more buzz")
    if key == keyboard.Key.ctrl_l:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False

        
def run_buzz_legit(port, stop_event):
    # print("alelelele")
    import RPi.GPIO as GPI
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)
    with keyboard.Listener(on_press=partial(on_press_real, port), on_release=partial(on_release_real, port)) as listener:
        listener.join()