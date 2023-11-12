import time
import random

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_ds_simulator(callback, stop_event):
    previous = 0;
    while True:
        pressed = random.randint(0, 1)
        # print(pressed)
        if (pressed==0 and previous==1):
            callback(None)
        # elif (pressed==0 and previous==1):
        #      print("zakljucano")
        if stop_event.is_set():
            break
        previous = pressed
        time.sleep(1)
              