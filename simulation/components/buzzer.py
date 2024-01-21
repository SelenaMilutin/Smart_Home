import json
import sys
import paho.mqtt.publish as publish
from server.messenger_sender import generate_payload
from simulation.mqtt_topics import BUZZER_ALARM_TOPIC, BUZZER_CLOCK_TOPIC
from simulators.buzzer import run_buzz_simulation
import threading
sys.path.append("../")
from broker_settings import HOSTNAME, PORT
import paho.mqtt.client as mqtt


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

param_settings = None   

def on_connect(client, userdata, flags, rc): 
    client.subscribe(BUZZER_ALARM_TOPIC)
    client.subscribe(BUZZER_CLOCK_TOPIC)

def on_message(client, userdata, msg):
    global param_settings
    decoded = msg.payload.decode('utf-8')
    if decoded == "activate":
        print("MESSAGE activate ALARM RECEIVED IN BUZZER")
        param_settings['on'] = True
        return
    if decoded == "deactivate":
        print("MESSAGE deactivate ALARM RECEIVED IN BUZZER")
        param_settings['on'] = False
        return

    if param_settings['name'] == 'BB':
        try:
            decoded_json = json.loads(decoded)
            print("MESSAGE clock set:", decoded_json['on'], decoded_json['hour'], decoded_json['minute'], " RECEIVED IN BUZZER")
            param_settings['clock'] = {'hour': decoded_json['hour'], 'minute': decoded_json['minute']} 
            if decoded_json['for'] == "off": # clock is turned off
                param_settings['on'] = False
        except json.JSONDecodeError:
            print("Error decoding JSON")



def run_buzzer(settings, threads, stop_event):

    global param_settings
    param_settings = settings
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    param_settings['clock'] = {'hour': -1, 'minute': -1} 

    if settings['simulated']:
        print("Starting buzz sumilator")
        buzz_thread = threading.Thread(target = run_buzz_simulation, args=(param_settings, callback, stop_event, publish_event))
        buzz_thread.start()
        threads.append(buzz_thread)
        print("Buzz sumilator started")
    else:
        from actuators.buzzer import run_buzz_legit
        print("Starting Buzz loop")
        buzz_thread = threading.Thread(target=run_buzz_legit, args=(param_settings, stop_event, publish_event, callback))
        buzz_thread.start()
        threads.append(buzz_thread)
        print("Buzz loop started")
