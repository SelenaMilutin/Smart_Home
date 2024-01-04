import random
import time


def run_bir_simulator(settings, callback, stop_event):
    """
        Simulates pressed buttons 0-9 in random interval (0-10 seconds).
    """
    while True:
        val = random.randint(0, 9)
        interval = random.randint(0,10)
        callback(val, settings, True)
        if stop_event.is_set():
                break
        time.sleep(interval)
      
              