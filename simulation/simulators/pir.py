import time
import random

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_pir_simulator(settings, callback, stop_event, publish_event):
    for detected in generate_values():
        if detected:
            # callback(settings, publish_event)
            isDPIR1 = True if settings.get("isDoor") != None and settings.get("isDoor") else False
            callback(settings, publish_event, isDPIR1=isDPIR1, verbose=True)
        if stop_event.is_set():
            break
        time.sleep(7)
              