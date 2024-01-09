import json
import sys
import paho.mqtt.client as mqtt


sys.path.append("../")
from broker_settings import HOSTNAME, PORT

humidity = 0
temp = 0

def run_display_simulator(settings, callback, stop_event):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    

    mqtt_client.loop_start()

    def on_connect(client, userdata, flags, rc): #subscribe na topike
        client.subscribe("temperature-GDHT")
        client.subscribe("humidity-GDHT")

    mqtt_client.on_connect = on_connect

    def on_message(client, userdata, msg):
        global humidity, temp

        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = json.loads(msg.payload.decode('utf-8'))
        if data["measurement"] == "temperature":
            humidity = data["value"]
        if data["measurement"] == "humidity":
            temp = data["value"]
        callback(humidity, temp, settings, True)

    mqtt_client.on_message = on_message
      
              