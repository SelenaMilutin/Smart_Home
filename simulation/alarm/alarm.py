import json
import threading
from broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish

from simulation.mqtt_topics import ALARM_ACTIVATION_TOPIC, BUZZER_ALARM_TOPIC

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
        print(f'published {publish_data_limit} alarm values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def publish_alarm(activate, simulated, component_name, runs_on):
    global publish_data_counter, publish_data_limit
    payload = {
        "measurement": "alarm",
        "value": 1 if activate=="activate" else 0,
        "simulated": simulated,
        "name": component_name,
        "runs_on": runs_on
    }
    with counter_lock:
        dht_batch.append(("alarmmm", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def publish_to_buzzer(activate):
    publish.single(BUZZER_ALARM_TOPIC, activate, hostname=HOSTNAME, port=PORT)


def activate_alarm(activate, simulated, component_name, runs_on, verbose = False):
    # activate: "activate" OR "deactivate"
    if verbose:
        print(f"Alarm")
        print("="*20)
    publish_alarm(activate, simulated, component_name, runs_on)
    publish_to_buzzer(activate)
