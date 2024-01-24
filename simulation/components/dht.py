
import sys
from server.messenger_sender import generate_payload
from simulators.dht import run_dht_simulator
import threading
import time
import paho.mqtt.publish as publish
sys.path.append("../")
from broker_settings import HOSTNAME, PORT


dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht_callback(humidity, temperature, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = generate_payload(temperature, dht_settings)

    humidity_payload = generate_payload(humidity, dht_settings, 1)


    with counter_lock:
        dht_batch.append((dht_settings["topic"][0], temp_payload, 0, True))
        dht_batch.append((dht_settings["topic"][1], humidity_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht simulator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(5, settings, dht_callback, stop_event, publish_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht simulator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print("Starting dht loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, settings, dht_callback, stop_event, publish_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht loop started")
