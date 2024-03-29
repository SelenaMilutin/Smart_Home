
import sys
import threading
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

sys.path.append("../")
from simulators.dms import run_dms_simulator
from server.messenger_sender import generate_dms_payload
from broker_settings import HOSTNAME, PORT
from mqtt_topics import DMS_PIN_REQUEST_TOPIC


dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit, param_settings
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dms values')
        param_settings['should_be_correct'] = False
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(pin_val, settings, publish_event, verbose = False):
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        print("DOOR MEMBRANE SWITCH")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Entered pin {pin_val}")
        print(f"Should be correct {settings['should_be_correct']}")
    payload = generate_dms_payload(str(pin_val), settings, pin_val == settings['pin'])
    with counter_lock:
        dht_batch.append((settings["topic"][0], payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def on_connect(client, userdata, flags, rc): 
    client.subscribe(DMS_PIN_REQUEST_TOPIC)


def on_message(client, userdata, msg):
    global param_settings
    print("MESSAGE PIN REQUEST RECEIVED IN DMS")
    param_settings['should_be_correct'] = True

param_settings = None

def run_dms(settings, threads, stop_event):
    global param_settings
    param_settings = settings
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    if settings['simulated']:
        print("Starting dms simulator")
        dms_thread = threading.Thread(target = run_dms_simulator, args=(param_settings, callback, stop_event, publish_event))
        dms_thread.start()
        threads.append(dms_thread)
        print("dms simulator started")
    else:
        from sensors.dms import run_dms_loop
        print("Starting dms loop")
        dms_thread = threading.Thread(target=run_dms_loop, args=(param_settings, callback, stop_event, publish_event))
        dms_thread.start()
        threads.append(dms_thread)
        print("dms loop started")
