# from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import sys


sys.path.append("../")
from broker_settings import HOSTNAME, INFLUX_TOKEN, BUCKET, ORG, INFLUXHOSTNAME
from alarm.alarm import activate_alarm

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
        activate_alarm("activate", data["simulated"], data["name"], data["runs_on"])

        return {"status": "error", "data": "alarm"}
    return {"status": "success", "data": "okej"}

def try_detection_DPIR(dus_id):
    nesto = get_data_DPIR('5s', 'distance', "DUS" + dus_id)
    save_people_num(nesto)

    return {"status": "success", "data": nesto}

def get_data_DPIR(time, measurement, device_name):
    data = get_data_by_time_measurment_device_name(time, measurement, device_name)
    # people_num = get_people_num()  #TODO da li treba lock, treba lock
    people_num = get_last_data("people_num")
    if not data or len(data) < 2 :
        return people_num
    if data[0].get("_value") <  data[-1].get("_value"):
        people_num = max(0, people_num - 1)
    if data[0].get("_value") >  data[-1].get("_value"):
        people_num += 1
        
    # save_settings({"PEOPLE_NUMBER": people_num}, "../house_info.json")
    return people_num

def process_entered_pin(data):
    # alarm_system_active = server.get_alarm_system_active()
        # activate alarm system
        # deactivate alarm system

    alarm_state = get_alarm_state()
    print("alarm state:", alarm_state)
    if alarm_state and data['correct_pin']:
        print("deactivation")
        activate_alarm("deactivate", data['simulated'], data['name'], data['runs_on'], True)

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
        |> range(start: -30d)  // Assuming a large enough time range
        |> filter(fn: (r) => r._measurement == "{measurement}")
        |> last(column: "_value")"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return 5 if not data else data[0].get("_value")


def get_sum_of_values_by_time_measurment_device_name(time, measurement, device_name):
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -{time})
        |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
        |> sum(column: "_value")"""
    returned = handle_influx_query(query)
    print(returned)
    data = returned.get("data")
    sum_of_values = 0 if not data else data[0].get("_value", 0)
    return sum_of_values


def get_sef_movement():
    sum = get_sum_of_values_by_time_measurment_device_name("5s", "rotation", "GSG")
    print(sum)
    return sum > 100
    
# def get_alarm_system_state(time, measurement, device_name):
#     query = f"""from(bucket: "{BUCKET}")
#         |> range(start: -{time})
#         |> filter(fn: (r) => r._measurement == "{measurement}" and r["name"] == "{device_name}")
#         |> last()"""
#     returned = handle_influx_query(query)
#     data = returned.get("data")
#     return {"status": "success", "data": data}

def get_alarm_state():
    query = f"""from(bucket: "{BUCKET}")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "alarm-state")
        |> last()"""
    returned = handle_influx_query(query)
    data = returned.get("data")
    return 0 if not data else data[0].get("_value")

def save_people_num(number):
    print('usao u save number')
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("people_num")
        .field("value", number)
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)


if __name__=="__main__":
    print(get_sef_movement())