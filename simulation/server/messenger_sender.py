import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from threading import Lock
from copy import deepcopy


mutex = Lock()

FLUSH_SIZE = 5
batch = []
def send_measurement(value, settings, topic_num=0):
    global batch
    print("usao")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.username_pw_set("admin", "1234")

    device_payload = generate_payload(value, settings, topic_num)

    batch_copy = []
    with mutex:
        batch.append((settings["topic"][topic_num], device_payload, 0, True))
        if len(batch) >= FLUSH_SIZE:
            batch_copy = deepcopy(batch)
            batch.clear()
            publish.multiple(batch_copy)


def generate_payload(value, settings, topic_num):
    payload = {
        "measurement": settings["measurement"][topic_num],
        "value": value,
        "simulated": settings["simulated"],
        "name": settings["name"],
        "runs_on": settings["runs_on"]
    }
    temperature_payload = json.dumps(payload)
    return temperature_payload
        

