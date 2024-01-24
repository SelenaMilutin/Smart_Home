# from flask import Flask, jsonify, request
import json
import threading
import time
import paho.mqtt.publish as publish

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import sys


sys.path.append("../")
from broker_settings import HOSTNAME, INFLUX_TOKEN, BUCKET, ORG, INFLUXHOSTNAME, PORT
from alarm.alarm import activate_alarm
from mqtt_topics import DMS_PIN_REQUEST_TOPIC, B4SD_CLOCK_TOPIC, BUZZER_CLOCK_TOPIC, RGB_TOPIC


url = f"http://{INFLUXHOSTNAME}:8086"
# # url = "http://10.1.121.45:8086"

influxdb_client = InfluxDBClient(url=url, token=INFLUX_TOKEN, org=ORG)
people_num = 5


# # Set up the application context
# with app.app_context():
def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=ORG)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return {"status": "success", "data": container}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def try_detection_RPIR(data):
    people_num = get_last_data("people_num")
    if people_num == 0:
        activate_alarm("activate", "Motion detected but no one in the house.")
        return True
    return False

def try_detection_DPIR(dus_id):
     people_num = get_data_DPIR('10s', 'distance', "DUS" + dus_id)
     save_people_num(people_num)

     return people_num

def get_data_DPIR(time, measurement, device_name):
        data = get_data_by_time_measurment_device_name(time, measurement, device_name)
        people_num = get_last_data("people_num")
        if not data or len(data) < 2 :
            return people_num
        if data[0].get("_value") <  data[-1].get("_value"):
            people_num = max(0, people_num - 1)
        if data[0].get("_value") >  data[-1].get("_value"):
            people_num += 1
        return people_num


def process_entered_pin(data):
    

    alarm_state = get_alarm_state()
    alarm_system_active = get_alarm_system_state()
    print("alarm state:", alarm_state)
    print("alarm system state:", alarm_system_active)
    print("pin correct: ", data['is_correct'])

    if data['is_correct']:
        if alarm_state: # deactivation
            print("alarm deactivation")
            activate_alarm("deactivate", "DMS pin entered.", verbose=True)
            if alarm_system_active:
                print("alarm system deactivation")
                save_alarm_system_state(0)
        else:
            print("alarm system activation")
            thread = threading.Thread(target=save_alarm_system_state, args=(1, 10))
            thread.start()
    else:
        if alarm_system_active == 1 and data['should_be_correct'] and not data['is_correct']:
            print("alarm activation because alarm system active and incorrect pin and should be correct")
            activate_alarm("activate", "DMS incorrect pin.", verbose=True)
    return {"status": "success", "data": "ok"}


def process_ds(data):

    alarm_system_active = get_alarm_system_state()
    if alarm_system_active == 1:
        publish.single(DMS_PIN_REQUEST_TOPIC, 1, hostname=HOSTNAME, port=PORT)
        print("pin request sent to DMS")
    return {"status": "success", "data": "ok"}

def get_data_by_time_measurment_device_name(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
        |> sort(columns: ["_time"], desc: false)"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return data

def get_last_data(measurement):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "{measurement}")
        |> last(column: "_value")"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return 5 if not data else data[0].get("_value")


def get_sum_of_values_by_time_measurment_device_name(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")"""
    returned = handle_influx_query(query)
    # print(returned)
    data = returned.get("data")
    sum = 0
    for record in data:
        all_three = record.get("_value")
        numbers = all_three.split(",")
        # print(numbers)
        for number in numbers:
            sum += abs(float(number))
    return sum


def is_sef_movement_important(data):
    sum_rot = get_sum_of_values_by_time_measurment_device_name("5s", data["measurement"][0], "GSG")
    sum_ac = get_sum_of_values_by_time_measurment_device_name("5s", data["measurement"][1], "GSG")
    # print("acel", sum_ac)
    print("rotat", sum_rot)
    # print(sum)
    if sum_rot > 100:
        activate_alarm("activate", "Gyroscope rotation detected.")
    else:
        if sum_ac > 4:
            activate_alarm("activate", "Gyroscope acceleration detected.")
    
    return sum_rot > 100
    
def get_alarm_system_state():
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "alarm-system")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return 0 if not data else data[0].get("_value")

def get_alarm_state():
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "alarm-state")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return 0 if not data else data[0].get("_value")

def get_last_set_clock():
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "clock")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return {"hour": -1, "minute": -1} if not data else {"hour": data[0].get("_value"), "minute":data[1].get("_value")}

def save_people_num(number):
    # print('usao u save number')
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("people_num")
        .field("value", number)
        # .field("value", number)
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)

def save_alarm_system_state(state, sleep=0):
    # state = 1 active
    # state = 0 deactivated
    time.sleep(sleep)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("alarm-system")
        .field("value", state)
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    print("saved alarm system state: ", state)


def save_clock(hour, minute):
    try:
        print("saving clock")

        # to database
        write_clock_db(hour, minute)

        # publish to devices
        publish.single(BUZZER_CLOCK_TOPIC, json.dumps({"hour": hour, "minute": minute, "for": "set"}), hostname=HOSTNAME, port=PORT)
        publish.single(B4SD_CLOCK_TOPIC, json.dumps({"hour": hour, "minute": minute, "for": "set"}), hostname=HOSTNAME, port=PORT)

        return {"status": "success", "data": "Clock set successfully."}
    except:
        return {"status": "fail", "data": "Error."}

def save_clock_off(cancel=True):
    try:
        print("saving clock off for cancel = ", cancel)
        for_reason = "cancel" if cancel else "off"

        write_clock_db(-1, -1)
        # publish to devices
        publish.single(BUZZER_CLOCK_TOPIC, json.dumps({"hour": -1, "minute": -1, "for": for_reason}), hostname=HOSTNAME, port=PORT)
        publish.single(B4SD_CLOCK_TOPIC, json.dumps({"hour": -1, "minute": -1, "for": for_reason}), hostname=HOSTNAME, port=PORT)

        return {"status": "success", "data": "Clock turned off successfully."}
    except:
        return {"status": "fail", "data": "Error."}

def write_clock_db(hour, minute):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("clock")
        .field("hour", hour)
        .field("minute", minute)
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)   


def publish_rgb(val):

    publish.single(RGB_TOPIC, val, hostname=HOSTNAME, port=PORT)


if __name__=="__main__":
    print(is_sef_movement_important())