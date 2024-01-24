import random
import threading
import time


def run_rgb_simulator(settings, callback, stop_event, publish_event):
    while True:
        callback(settings["val"], settings["on"], settings, publish_event)
        if stop_event.is_set():
            return
        time.sleep(1)
        