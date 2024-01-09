import sys
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from flask_cors import CORS
from queries import try_detection_DPIR, influxdb_client
sys.path.append("../")
from settings import load_settings, save_settings
from broker_settings import HOSTNAME, PORT, INFLUX_TOKEN, BUCKET, ORG, people_num



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

url = f"http://{HOSTNAME}:8086"
# url = "http://10.1.121.45:8086"

# influxdb_client = InfluxDBClient(url=url, token=INFLUX_TOKEN, org=ORG)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)

# mqtt_client.connect("10.1.121.102", 1883, 60)

mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc): #subscribe na topike
    get_people_num()
    settings = load_settings(filePath='../settings.json')
    for device in settings:
        for topic in settings[device]["topic"]:
            client.subscribe(topic)
    client.subscribe("alarmmm")

mqtt_client.on_connect = on_connect

def on_message(client, userdata, msg):
    # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    data = json.loads(msg.payload.decode('utf-8'))
    proces(data)
    save_to_db(data)

mqtt_client.on_message = on_message

def get_people_num():
     settings = load_settings(filePath='../house_info.json')
     global people_num
     people_num = settings['PEOPLE_NUMBER']
     return settings['PEOPLE_NUMBER']

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected'})

def emit_updated_data(data):
    socketio.emit('updated_data', {'data': data})

def proces(data):
     if data["measurement"] == "realised" and data["name"].startswith("D"):
        print("nesto je uradio")
        nesto = try_detection_DPIR(data["name"][-1])
        print(nesto)
        emit_updated_data({"status": "success", "data": nesto});


def save_to_db(data):
    # print(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("value", data["value"])
    )
    write_api.write(bucket=BUCKET, org=ORG, record=point)

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



if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)