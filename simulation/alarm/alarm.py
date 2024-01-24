import json
import sys
import threading
from broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import sys 

sys.path.append("../")
from mqtt_topics import ALARM_ACTIVATION_TOPIC, BUZZER_ALARM_TOPIC
from server.messenger_sender import generate_alarm_payload

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

def publish_alarm(activate, reason):
    global publish_data_counter, publish_data_limit
    payload = generate_alarm_payload(1 if activate=="activate" else 0, reason)
    with counter_lock:
        dht_batch.append(("alarmmm", payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def publish_to_buzzer(activate):
    publish.single(BUZZER_ALARM_TOPIC, activate, hostname=HOSTNAME, port=PORT)


def activate_alarm(activate, reason="", verbose = False):
    # activate: "activate" OR "deactivate"
    if verbose:
        print(f"Alarm")
        print("="*20)
        print(activate)
    # if component_name == "DS1" or "DS2" and ! alarm system active: 
        # return 
    publish_alarm(activate, reason)
    publish_to_buzzer(activate)

