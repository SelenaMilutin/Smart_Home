import time
import random


def generate_values():
      dist = 0
      while True:
            change = random.uniform(-5, 5)
            if (dist + change < 0 or dist + change > 10) : 
                # dist > 10 meters - object is no longer registered
                dist = 0 
                continue
            dist += change
            yield dist


def run_dus_simulator(settings, callback, stop_event, publish_event):
    for val in generate_values():
        callback(val, settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(2)