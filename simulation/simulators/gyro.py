import random
import time

def generate_values(initial_rotation = 0, initial_acceleration = 0):
      rotation = initial_rotation
      acceleration = initial_acceleration 
      i = 0
      while True:
            if i%6==0:
                i += 1
                yield 100, 100
            rotation = rotation + random.randint(-1, 1)
            acceleration = acceleration + random.randint(-1, 1)
            if acceleration < 0:
                  acceleration = 0
            if acceleration > 10:
                  acceleration = 10
            i += 1
            yield rotation, acceleration

def run_gyro_simulation(delay, settings, callback, stop_event, publish_event):
    for rotation, acceleration in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(rotation, acceleration, publish_event, settings)
            if stop_event.is_set():
                  break