

from simulators.dht import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("DHT")
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht simulator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(5, settings, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht simulator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print("Starting dht loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, settings, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht loop started")
