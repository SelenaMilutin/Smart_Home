import time
import random

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_ds_simulator(callback, stop_event):
    previous = False;
    for pressed in generate_values():
        if (pressed and not previous):
            callback(None)
        if stop_event.is_set():
            break
        previous = pressed
        time.sleep(1)
              