import sys
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

def proces(data):
    # print("u proces", type(data), data)
    if (type(data)==str):
        data = json.loads(data)
    if data["measurement"] == "realised" and data["name"].startswith("DPIR"):
        print("DPIR function")
        nesto = try_detection_DPIR(data["name"][-1])
        print(nesto)
        emit_updated_data({"status": "success", "data": nesto})
    if data["measurement"] == "realised" and data["name"].startswith("RPIR"):
        print("RPIR function")
        nesto = try_detection_RPIR(data)
        print(nesto)
        emit_updated_data({"status": "success", "data": nesto})
    if data["measurement"] == "entered-pin" and data["name"].startswith("DMS"):
        process_entered_pin(data)
    if data["measurement"] == "motion" and data["name"].startswith("DS"):
        if BUCKET == "iot":
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
                'topic': settings[device]['topic']
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
    if (hour > 23 or hour < 0) or (minute > 59 or minute < 0):
        return {"status": "fail", "data": "Wrong fields."}
    return jsonify(save_clock(hour, minute))

@app.route('/clock-off', methods=['PUT'])
def set_clock_off():
    return jsonify(save_clock_off())

@app.route('/alarm-state', methods=['GET'])
def get_last_clock():
    return json.dumps({'data': get_last_set_clock()})

@app.route('/alarm-off', methods=['PUT'])
def set_alarm_off():
    print("clicked alarm off")
    activate_alarm("deactivate", verbose=True)
    return {"status": "success", "data": "Alarm turned off."}

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)