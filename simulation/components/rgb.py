import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from server.messenger_sender import generate_payload
from broker_settings import HOSTNAME, PORT
from simulation.mqtt_topics import RGB_TOPIC
from simulation.simulators.rgb import run_rgb_simulator

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
        print(f'published {publish_data_limit} rgb values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(rgb_val, on_val, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        print("="*20)
        print("RGB")
        print(f"RGB Value: {rgb_val}")
        print(f"On/Off Value: {on_val}")

    val_payload = generate_payload(int(rgb_val), settings, 0)
    on_payload = generate_payload(on_val, settings, 1)

    with counter_lock:
        dht_batch.append((settings["topic"][0], val_payload, 0, True))
        dht_batch.append((settings["topic"][1], on_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def on_connect(client, userdata, flags, rc): 
    client.subscribe(RGB_TOPIC)


def on_message(client, userdata, msg):
    global param_settings
    decoded = msg.payload.decode('utf-8')
    print(f"MESSAGE {decoded} RECEIVED IN RGB")
    if decoded == "0":
        param_settings["on"] = 0
        param_settings["val"] = "-1"
    elif decoded == "1":
        param_settings["on"] = 1
        # Turn on and set color to default
        param_settings["val"] = "2"
    else:
        # Light is on and color can be changed
        if param_settings["on"] == 1:
            param_settings["val"] = decoded
        

param_settings = None

def run_rgb(settings, threads, stop_event):
    global param_settings
    param_settings = settings

    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    if settings['simulated']:
        print("Starting RGB simulator")
        rbg_thread = threading.Thread(target = run_rgb_simulator, args=(param_settings, rgb_callback, stop_event, publish_event))
        rbg_thread.start()
        threads.append(rbg_thread)
        print("RGB simulator started")
    else:
        print("Starting RGB loop")
        rbg_thread = threading.Thread(target=run_rgb_loop, args=(param_settings, rgb_callback, stop_event, publish_event))
        rbg_thread.start()
        threads.append(rbg_thread)
        print("RGB display loop started")