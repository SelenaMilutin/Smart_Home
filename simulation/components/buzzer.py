import sys
import paho.mqtt.publish as publish
from server.messenger_sender import generate_payload
from simulators.buzzer import run_buzz_simulation
import threading
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
        print(f'published {publish_data_limit} buzz values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def callback(val, settings, publish_event, verbose = False):
    global publish_data_counter, publish_data_limit
    # t = time.localtime()
    if verbose:
        print("BUZZER")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Entered pin {pin_val}")
        print(f"Buzzer {val}")
    button_payload = generate_payload(val, settings)
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


     

def run_buzzer(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting buzz sumilator")
            buzz_thread = threading.Thread(target = run_buzz_simulation, args=(settings, callback, stop_event, publish_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz sumilator started")
        else:
            from actuators.buzzer import run_buzz_legit
            print("Starting Buzz loop")
            buzz_thread = threading.Thread(target=run_buzz_legit, args=(settings, stop_event, publish_event, callback))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz loop started")
