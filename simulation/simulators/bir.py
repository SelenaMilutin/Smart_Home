import random
import time
from simulation.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish

from simulation.mqtt_topics import RGB_TOPIC

def run_bir_simulator(settings, callback, stop_event):
    """
        Simulates pressed buttons 0-9 in random interval (0-10 seconds).
    """
    # Turn on light at start of simulation
    publish.single(RGB_TOPIC, 1, hostname=HOSTNAME, port=PORT)

    while True:
        val = random.randint(0, 9)
        interval = random.randint(0,10)
        callback(val, settings, True)
        # For communication to BGR
        publish.single(RGB_TOPIC, val, hostname=HOSTNAME, port=PORT)
        if stop_event.is_set():
                break
        time.sleep(interval)
      
              