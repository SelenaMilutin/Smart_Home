import time
import random

from server.messenger_sender import send_measurement

def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_ds_simulator(settings, callback, stop_event):
    previous = 0;
    while True:
        pressed = random.randint(0, 1)
        # print(pressed)
        if (pressed==0 and previous==1):
            callback(None)
            send_measurement(1, settings)
            
        # elif (pressed==0 and previous==1):
        #      print("zakljucano")
        if stop_event.is_set():
            break
        previous = pressed
        time.sleep(1)
              