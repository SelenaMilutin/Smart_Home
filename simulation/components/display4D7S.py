import threading
import time
import json

from simulation.simulators.display4D7S import run_display_simulator
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT
from simulation.mqtt_topics import B4SD_CLOCK_TOPIC

def display_callback(timestamp, display_settings, verbose=False):

    if verbose:
        t = time.localtime()
        print("="*20)
        print("4D7S display")
        print(f"Timestamp: {time.strftime('%H:%M', timestamp)}")
        if display_settings['blink']:
            print(f"CURRENTLY BLINKING BECAUSE OF CLOCK ACTIVATED")

param_settings = None   

def on_connect(client, userdata, flags, rc): 
    client.subscribe(B4SD_CLOCK_TOPIC)

def on_message(client, userdata, msg):
    global param_settings
    decoded = msg.payload.decode('utf-8')
    try:
        decoded_json = json.loads(decoded)
        print("MESSAGE clock set:", decoded_json['on'], decoded_json['hour'], decoded_json['minute'], " RECEIVED IN BUZZER")
        param_settings['clock'] = {'hour': decoded_json['hour'], 'minute': decoded_json['minute']} 
        if decoded_json['for'] == "off": # clock is turned off
            param_settings['blink'] = False
    except json.JSONDecodeError:
        print("Error decoding JSON")
      

def run_4D7Sdisplay(settings, threads, stop_event):

    global param_settings
    param_settings = settings
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    param_settings['clock'] = {'hour': -1, 'minute': -1} 
    
    if settings['simulated']:
        print("Starting 4D7S display simulator")
        display_thread = threading.Thread(target = run_display_simulator, args=(settings, display_callback, stop_event))
        display_thread.start()
        threads.append(display_thread)
        print("4D7S display simulator started")
    else:
        from actuators.display4D7S import run_display_loop
        print("Starting 4D7S display loop")
        display_thread = threading.Thread(target=run_display_loop, args=(settings, display_callback, stop_event))
        display_thread.start()
        threads.append(display_thread)
        print("4D7S display loop started")