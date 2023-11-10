import threading
import time
from pynput import keyboard
from functools import partial

# def ctrl(letter): return chr(ord(letter.upper())-64)

def on_press(key):
    print(key)
    if key == "x03":
        keyboard.Listener.stop
        print("ugasena je tastatura")
    if key == keyboard.Key.space:
        print("Buzzzz")
    
def on_release(key):
    if key == keyboard.Key.space:
        print("No more buzz")
    if key == keyboard.Key.backspace:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False
    

def on_press_real(port, key):
    if key == keyboard.Key.space:
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
    if key == keyboard.Key.backspace:
        keyboard.Listener.stop
        print("ugasena je tastatura")
        return False



def run_buzzer(settings, threads, stop_event):
        print("!!!!!!!!!!!!!!!!!!!!!!")
        print("SA SPACE SE PALI A BACSPACE ISKLJUCUJE SLUSANJE ZA TASTATURU ZA SAD")
        if settings['simulated']:
            print("Starting buzz sumilator")
            buzz_thread = threading.Thread(target = run_buzz_simulation, args=(on_press, on_release, stop_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz sumilator started")
        else:
            print("Starting Buzz loop")
            buzz_thread = threading.Thread(target=run_buzz_legit, args=(settings['pin'], on_press_real, on_release_real, stop_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz loop started")



def run_buzz_simulation(on_press_callback, on_release_callback, stop_event):
    with keyboard.Listener(on_press=on_press_callback, on_release=on_release_callback) as listener:
        listener.join()
        if stop_event.is_set():
            keyboard.Listener.stop
            return
        
def run_buzz_legit(port, on_press_callback, on_release_callback, stop_event):
    import RPi.GPIO as GPI
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)
    with keyboard.Listener(on_press=partial(on_press_callback, port), on_release=partial(on_release_callback, port)) as listener:
        listener.join()