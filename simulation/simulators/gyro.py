import random
import time

def generate_values(initial_rotation = 0, initial_acceleration = 0):
      rotation = initial_rotation
      acceleration = initial_acceleration 
      i = 0
      while True:
            if i%6==0:
                i += 1
                yield 200, 4
            rotation = rotation + random.randint(-1, 1)
            acceleration = acceleration + random.randint(-1, 1)
            if acceleration < -2:
                  acceleration = -2
            if acceleration > 2:
                  acceleration = 2
            i += 1
            yield rotation, acceleration

def run_gyro_simulation(delay, settings, callback, stop_event, publish_event):
    for rotation, acceleration in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(f"{rotation},0,0", f"{acceleration},0,0", publish_event, settings)
            if stop_event.is_set():
                  break