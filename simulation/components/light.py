

import sys
import time
from server.messenger_sender import generate_payload
from simulators.light import run_light_simulator
import threading
import paho.mqtt.publish as publish
sys.path.append("../")
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

param_settings = None
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
        print(f'published {publish_data_limit} light values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(val, settings, publish_event, verbose = False):
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        # print("LIGHT")
        # print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Entered pin {pin_val}")
        print(f"Light {val}")
    print(f"Light {val}")
    button_payload = generate_payload(val, settings)
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def on_connect(client, userdata, flags, rc): 
    client.subscribe("dl")


def on_message(client, userdata, msg):
    global param_settings
    decoded = msg.payload.decode('utf-8')
    if decoded == "on":
        print("MESSAGE LIGHT {val} RECEIVED IN LIGHT")
        param_settings['on'] = True
        time.sleep(10)
        param_settings['on'] = False


def run_light(settings, threads, stop_event):
    global param_settings
    param_settings = settings
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    if settings['simulated']:
        print("Starting light simulator")
        light_thread = threading.Thread(target = run_light_simulator, args=(param_settings, callback, stop_event, publish_event))
        light_thread.start()
        threads.append(light_thread)
        print("light simulator started")
    else:
        from actuators.light import run_light_loop
        print("Starting light loop")
        light_thread = threading.Thread(target=run_light_loop, args=(param_settings, callback, stop_event, publish_event))
        light_thread.start()
        threads.append(light_thread)
        print("light loop started")
