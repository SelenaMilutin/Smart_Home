import sys
import paho.mqtt.publish as publish
from server.messenger_sender import generate_payload
from simulators.gyro import run_gyro_simulation
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
        print(f'published {publish_data_limit} gyro values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def callback(rotation, acceleration, publish_event, settings, verbose = False):
    global publish_data_counter, publish_data_limit
    # t = time.localtime()
    if verbose:
        print("GYRO")
        print("="*20)
        # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        # print(f"Entered pin {pin_val}")
        print(f"Gyro roation {rotation}")
        print(f"Gyro acceleration {acceleration}")
    rotation_payload = generate_payload(rotation, settings)
    acceleration_payload = generate_payload(acceleration, settings, 1)
    with counter_lock:
        dht_batch.append((settings["topic"][0], rotation_payload, 0, True))
        dht_batch.append((settings["topic"][1], acceleration_payload, 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


     

def run_gyro(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting gyro sumilator")
            buzz_thread = threading.Thread(target = run_gyro_simulation, args=(5, settings, callback, stop_event, publish_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Gyro sumilator started")
        else:
            from sensors.MPU6050.gyro import run_gyro_loop
            print("Starting gyro loop")
            buzz_thread = threading.Thread(target=run_gyro_loop, args=(settings, stop_event, publish_event, callback))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Gyro loop started")
