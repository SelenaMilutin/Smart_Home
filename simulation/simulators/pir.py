import time
import random

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_pir_simulator(settings, callback, stop_event, publish_event):
    for pressed in generate_values():
        if pressed:
            callback(settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(5)
              