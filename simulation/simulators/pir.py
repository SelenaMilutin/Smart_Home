import time
import random

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_pir_simulator(callback, stop_event):
    for pressed in generate_values():
        if pressed:
            callback(None)
        if stop_event.is_set():
            break
        time.sleep(1)
              