import time
import random

from server.messenger_sender import send_measurement

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature, "DHTLIB_OK"

      

def run_dht_simulator(delay, settings, callback, stop_event):
        for h, t, c in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(h, t, c)
            send_measurement(t, settings)
            send_measurement(h, settings, topic_num=1)
            if stop_event.is_set():
                  break
              