import time
import random

def generate_values():
      dist = 0
      while True:
            change = random.uniform(-5, 5)
            if (dist + change < 0): dist = 0
            else: dist += change
            yield dist


def run_dus_simulator(callback, stop_event):
    for val in generate_values():
        callback(val)
        if stop_event.is_set():
            break
        time.sleep(1)