# from flask import Flask, jsonify, request
import threading
from influxdb_client import InfluxDBClient
import sys

sys.path.append("../")
from broker_settings import HOSTNAME, INFLUX_TOKEN, BUCKET, ORG, INFLUXHOSTNAME

url = f"http://{INFLUXHOSTNAME}:8086"
# # url = "http://10.1.121.45:8086"

influxdb_client = InfluxDBClient(url=url, token=INFLUX_TOKEN, org=ORG)
people_num = 5
counter_lock = threading.Lock()


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


def try_detection_RPIR():
     global people_num
     if people_num == 0:
        return {"status": "error", "data": "alarm"}
     return {"status": "success", "data": "okej"}

def try_detection_DPIR(dus_id):
     nesto = get_data_DPIR('5s', 'distance', "DUS" + dus_id)
     return {"status": "success", "data": nesto}

def get_data_DPIR(time, measurement, device_name):
        data = get_data_by_time_measurment_device_name(time, measurement, device_name)
        # people_num = get_people_num()  #TODO da li treba lock, treba lock
        global people_num
        with counter_lock:
            if not data or len(data) < 2 :
                return people_num
            if data[0].get("_value") <  data[-1].get("_value"):
                people_num = max(0, people_num - 1)
            if data[0].get("_value") >  data[-1].get("_value"):
                people_num += 1
        # save_settings({"PEOPLE_NUMBER": people_num}, "../house_info.json")
        return people_num

def get_data_by_time_measurment_device_name(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
        |> sort(columns: ["_time"], desc: false)"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return data

def get_sef_movement():
    records = get_data_by_time_measurment_device_name("5s", "rotation", "GSG")
    value = 0
    for record in records:
        value += record.get("_value")
    return value < 100
    
def get_alarm_system_state(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return {"status": "success", "data": data}

def get_alarm_state(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return {"status": "success", "data": data}

if __name__=="__main__":
    print(try_detection_DPIR())