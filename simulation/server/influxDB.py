import signal
import sys
from threading import Thread
import time
import schedule
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from flask_cors import CORS
from queries import *
sys.path.append("../")
from settings import load_settings, save_settings
from mqtt_topics import DMS_PIN_REQUEST_TOPIC
from broker_settings import HOSTNAME, PORT, BUCKET, ORG, people_num, INFLUXHOSTNAME
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")

url = f"http://{HOSTNAME}:8086"
# url = "http://10.1.121.45:8086"

# influxdb_client = InfluxDBClient(url=url, token=INFLUX_TOKEN, org=ORG)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)

# mqtt_client.connect("10.1.121.102", 1883, 60)
def get_data_gyro():
    settings = load_settings(filePath='../settings.json')
    for device in settings:
        if settings[device]["name"] == "GSG":
            return settings[device]


mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc): #subscribe na topike
    settings = load_settings(filePath='../settings.json')
    for device in settings:
        for topic in settings[device]["topic"]:
            client.subscribe(topic)
    client.subscribe("alarmmm")

mqtt_client.on_connect = on_connect

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    # print("u on message payload", type(payload), payload)
    data = json.loads(payload)
    # print("u on message", type(data), data)
    proces(data)
    # if (type(data)==str):
    #     data = json.loads(data)
    if data['measurement'] == "alarm-state":
        save_alarm(data)
        return
    save_to_db(data)
    emit_table_data({"for": data['name'], "value": data["value"]})

mqtt_client.on_message = on_message

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected'})

@socketio.on('message_from_client')
def handle_message(message):
    print('Received message:', message)

    # Broadcast the received message to all connected clients
    emit('message_from_server', {'data': "Hello from server"}, broadcast=True)

def emit_updated_data(data):
    socketio.emit('updated_data', {'data': data})

def emit_table_data(data):
    socketio.emit('table_data', {'data': data})

def emit_alarm(data):
    socketio.emit('alarm', {'data': data})

def emit_lcd_data(data):
    socketio.emit('lcd', {'data': data})


def proces(data):
    if data["measurement"] == "realised" and data["name"].startswith("DPIR"):
        # print("DPIR function")
        people_num = try_detection_DPIR(data["name"][-1])
        emit_updated_data({"from": data["name"], "people_num": people_num});
    if data["measurement"] == "realised" and data["name"].startswith("RPIR"):
        # print("RPIR function")
        isAlarmActivated = try_detection_RPIR(data)
        if isAlarmActivated: #TODO move logic elsewhere
            emit_alarm({"from": data["name"], "reason": "Room Pir detected movement but no one is in the house"});
    if data['name'] == "GDHT":
         emit_lcd_data({"for": data['measurement'], "value": data["value"]})
    
    # print("u proces", type(data), data)
    if (type(data)==str):
        data = json.loads(data)
    if data["measurement"] == "entered-pin" and data["name"].startswith("DMS"):
        process_entered_pin(data)
    if data["measurement"] == "motion" and data["name"].startswith("DS"):
        if ORG == "my-influx":
            data["value"] = True
        process_ds(data)


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("value", data["value"])
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)

def save_alarm(data):
    if (type(data)==str):
        data = json.loads(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .field("value", data["value"])
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    socketio.emit('alarm-socket', json.dumps({'data': str(data["value"])}))


@app.route('/pir', methods=['GET'])
def store_data():
    return jsonify(try_detection_DPIR())



def check_sef():
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    data = get_data_gyro()
    is_important = is_sef_movement_important(data)
    if is_important:
        emit_alarm({"from": data["name"], "reason": "Sef moved"});

        


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_sef, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
# # Route to store dummy data
# @app.route('/store_data', methods=['POST'])
# def store_data():
#     try:
#         data = request.get_json()
#         store_data(data)
#         return jsonify({"status": "success"})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})


# def handle_influx_query(query):
#     try:
#         query_api = influxdb_client.query_api()
#         tables = query_api.query(query, org=org)

#         container = []
#         for table in tables:
#             for record in table.records:
#                 container.append(record.values)

#         return jsonify({"status": "success", "data": container})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})


# @app.route('/simple_query', methods=['GET'])
# def retrieve_simple_data():
#     query = f"""from(bucket: "{bucket}")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "{request.args.get("measurement")}")"""
#     return handle_influx_query(query)


# @app.route('/aggregate_query/', methods=['GET'])
# def retrieve_aggregate_data():
#     query = f"""from(bucket: "{bucket}")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "{request.args.get("measurement")}")
#     |> mean()"""
#     return handle_influx_query(query)
    
@app.route('/component/<piName>', methods=['GET'])
def retrieve_aggregate_data(piName):
    devices = []
    settings = load_settings(filePath='../settings.json')
    for device in settings:
        if settings[device]['runs_on'] == piName:
            devices.append({
                'code': device,
                'simulated': settings[device]['simulated'],
                'runsOn': settings[device]['runs_on'],
                'name': settings[device]['name'],
                'measurement': settings[device]['measurement'],
                'topic': settings[device]['topic'],
                'value': 0
            })
    # print(jsonify(devices))
    return jsonify(devices)

@app.route('/alarm-system-state', methods=['GET'])
def get_alarm_system_active():
    return json.dumps({'data': str(get_alarm_system_state())})


@app.route('/alarm-state', methods=['GET'])
def get_alarm_state_active():
    return json.dumps({'data': str(get_alarm_state())})

@app.route('/clock', methods=['POST'])
def set_clock():
    hour = int(request.json.get('hour'))
    minute = int(request.json.get('minute'))
    print(hour, minute)
    if (hour > 23 or hour < 0) or (minute > 59 or minute < 0):
        return {"status": "fail", "data": "Wrong fields."}
    return jsonify(save_clock(hour, minute))

@app.route('/clock-off', methods=['PUT'])
def set_clock_off():
    reason = request.json.get('reason')
    cancel = True if reason == 'cancel' else False
    return jsonify(save_clock_off(cancel))

@app.route('/last-clock', methods=['GET'])
def get_last_clock():
    return json.dumps({'data': get_last_set_clock()})

@app.route('/alarm-off', methods=['PUT'])
def set_alarm_off():
    print("clicked alarm off")
    activate_alarm("deactivate", verbose=True)
    return {"status": "success", "data": "Alarm turned off."}

@app.route('/rgb', methods=['PUT'])
def set_rgb():
    val = request.json.get('val')
    publish_rgb(val)
    return {"status": "success", "data": "RGB set."}

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)