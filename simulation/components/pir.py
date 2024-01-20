

import sys
from simulation.mqtt_topics import DOOR_LIGHT_TOPIC
from simulators.pir import run_pir_simulator
import threading
import time
from server.messenger_sender import generate_payload
import paho.mqtt.publish as publish
sys.path.append("../")
from broker_settings import HOSTNAME, PORT


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
        print(f'published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()



def callback_room_pir(settings, publish_event, verbose = False):
        
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        print("ROOM PASSIVE INFRARED SENSOR")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Motion detected in room")
    button_payload = generate_payload(1, settings)
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def callback_door_pir(settings, publish_event, isDPIR1 = False, verbose = False):
    global publish_data_counter, publish_data_limit
    if verbose:
        # t = time.localtime()
        print("DOOR PASSIVE INFRARED SENSOR")
        print(settings["name"])
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Motion detected in room")
    button_payload = generate_payload(1, settings)
    # data = get_data_by_time_measurment_device_name("5s", "distance", "DUS" + settings["name"][-1])
    with counter_lock:
        dht_batch.append((settings["topic"][0], button_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    if isDPIR1:
        # print("DoorPir callback, followed by MESSAGE LIGHT")
        publish.single(DOOR_LIGHT_TOPIC, "on", hostname=HOSTNAME, port=PORT)



def run_pir(settings, threads, stop_event, location, isDPIR1 = False):
        if settings['simulated']:
            print("Starting pir simulator")
            if location == "room":
                rpir_thread = threading.Thread(target = run_pir_simulator, args=(settings, callback_room_pir, stop_event, publish_event))
            else:
                rpir_thread = threading.Thread(target = run_pir_simulator, args=(settings, callback_door_pir, stop_event, publish_event))
            rpir_thread.start()
            threads.append(rpir_thread)
            print("Rpir1 sumilator started")
        else:
            from sensors.pir import run_pir_loop
            print("Starting pir loop")
            if location == "room":
                rpir_thread = threading.Thread(target=run_pir_loop, args=(settings, callback_room_pir, stop_event, publish_event))
            else:
                rpir_thread = threading.Thread(target=run_pir_loop, args=(settings, callback_door_pir, stop_event, publish_event))
            rpir_thread.start()
            threads.append(rpir_thread)
            print("Rpir1 loop started")
