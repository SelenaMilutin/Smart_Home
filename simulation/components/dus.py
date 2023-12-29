import threading
from simulators.dus import run_dus_simulator
import sys
import paho.mqtt.publish as publish
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
        print(f'published {publish_data_limit} dus values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dus_callback(val, settings, publish_event, verbose = False):
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        print("DOOR ULTRASONIC SENSOR")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Distance: {val}")
    button_payload = generate_payload(val, settings)
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dus simulator")
            dus_thread = threading.Thread(target = run_dus_simulator, args=(settings, dus_callback, stop_event, publish_event))
            dus_thread.start()
            threads.append(dus_thread)
            print("dus simulator started")
        else:
            from sensors.dus import run_dus_loop
            print("Starting dus loop")
            dus_thread = threading.Thread(target=run_dus_loop, args=(settings, dus_callback, stop_event, publish_event))
            dus_thread.start()
            threads.append(dus_thread)
            print("dus loop started")
