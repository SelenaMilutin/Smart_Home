import copy
import time
import random

def generate_values(settings):
    while True:
        pin = ""
        for i in range(4):
            rnd = random.randint(0, 9)
            pin += str(rnd)
            time.sleep(1)
        if (random.randint(1, 5) == 2):  # 10% chance that correct pin is entered
            pin = settings['pin']
        yield pin

def run_dms_simulator(settings, callback, stop_event, publish_event):

    for val in generate_values(settings):
        callback(val, settings, publish_event, True)
        if stop_event.is_set():
            break
        time.sleep(10)

   
              