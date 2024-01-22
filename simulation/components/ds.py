
import paho.mqtt.publish as publish
import sys
from simulators.ds import run_ds_simulator
import threading
from server.messenger_sender import generate_payload
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
        print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def callback(settings, publish_event, value = 1, verbose = False):
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        print("BUTTON")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Door open")
    button_payload = generate_payload(value, settings)
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ds(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting ds1 simulator")
            ds1_thread = threading.Thread(target = run_ds_simulator, args=(settings, callback, stop_event, publish_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Ds1 simulator started")
        else:
            from sensors.ds import run_ds_loop
            print("Starting ds1 loop")
            ds1_thread = threading.Thread(target=run_ds_loop, args=(settings, threads, callback, stop_event, publish_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Ds1 loop started")
