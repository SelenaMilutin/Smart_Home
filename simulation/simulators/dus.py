import time
import random

def generate_values():
      dist = 0
      while True:
            change = random.uniform(-5, 5)
            if (dist + change < 0): dist = 0
            if (dist + change > 10): dist = 0   # dist > 10 meters - object is no longer registered
            else: dist += change
            yield dist


def run_dus_simulator(callback, stop_event):
    for val in generate_values():
        callback(val)
        if stop_event.is_set():
            break
        time.sleep(1)