import json
from threading import Lock
from copy import deepcopy

from broker_settings import HOSTNAME, PORT


mutex = Lock()

FLUSH_SIZE = 5
batch = []
def send_measurement(value, settings, topic_num=0):
    global batch
    print("NE U OVO")
    # client = mqtt.Client()
    # client.connect(HOSTNAME, PORT, 60)

    # # client.connect("10.1.121.102", 1883, 60)

    # client.username_pw_set("admin", "1234")

    # device_payload = generate_payload(value, settings, topic_num)

    # batch_copy = []
    # with mutex:
    #     batch.append((settings["topic"][topic_num], device_payload, 0, True))
    #     if len(batch) >= FLUSH_SIZE:
    #         batch_copy = deepcopy(batch)
    #         batch.clear()
    #         publish.multiple(batch_copy, hostname=HOSTNAME, port=PORT)


def generate_payload(value, settings, topic_num=0):
    payload = {
        "measurement": settings["measurement"][topic_num],
        "value": value,
        "simulated": settings["simulated"],
        "name": settings["name"],
        "runs_on": settings["runs_on"]
    }
    temperature_payload = json.dumps(payload)
    return temperature_payload
        
def generate_alarm_payload(value, reason):
    payload = {
        "measurement": 'alarm-state',
        "value": value,
        "reason": reason
    }
    ret_payload = json.dumps(payload)
    return ret_payload

def generate_dms_payload(value, settings, is_correct_pin, topic_num=0):
    payload = {
        "measurement": settings["measurement"][topic_num],
        "value": value,
        "simulated": settings["simulated"],
        "name": settings["name"],
        "is_correct": is_correct_pin,
        "should_be_correct": settings["should_be_correct"],
        "runs_on": settings["runs_on"]
    }
    temperature_payload = json.dumps(payload)
    return temperature_payload
