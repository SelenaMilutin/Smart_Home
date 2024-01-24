import threading
import time
import paho.mqtt.publish as publish
from server.messenger_sender import generate_payload
from broker_settings import HOSTNAME, PORT
from simulation.sensors.bir import run_bir_loop
from simulation.simulators.bir import run_bir_simulator

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
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


def bir_callback(pressed, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        print("="*20)
        print("Bedroom infrared")
        print(f"Pressed value: {pressed}")
        print(f"Timestamp: {time.strftime('%H:%M', time.localtime())}")

    val = pressed
    payload = generate_payload(val, settings)

    with counter_lock:
        dht_batch.append((settings["topic"][0], payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_bir(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting BIR simulator")
            bir_thread = threading.Thread(target = run_bir_simulator, args=(settings, bir_callback, stop_event))
            bir_thread.start()
            threads.append(bir_thread)
            print("BIR simulator started")
        else:
            print("Starting BIR loop")
            bir_thread = threading.Thread(target=run_bir_loop, args=(settings, bir_callback, stop_event, publish_event))
            bir_thread.start()
            threads.append(bir_thread)
            print("BIR display loop started")