#!/usr/bin/env python3


from time import sleep, strftime
from datetime import datetime
from .Adafruit_LCD1602 import Adafruit_CharLCD

from .PCF8574 import PCF8574_GPIO
import json
import sys
import paho.mqtt.client as mqtt


sys.path.append("../")
from broker_settings import HOSTNAME, PORT

humidity = 0
temp = 0
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        #lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )# display CPU temperature
        lcd.message( get_time_now() )   # display the time
        sleep(1)


def poject_loop(settings, callback, stop_event):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)

    mqtt_client.loop_start()

    def on_connect(client, userdata, flags, rc): #subscribe na topike
        client.subscribe("temperature-GDHT")
        client.subscribe("humidity-GDHT")

    mqtt_client.on_connect = on_connect

    def on_message(client, userdata, msg):
        global humidity, temp

        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        
        data = json.loads(msg.payload.decode('utf-8'))
        if data["name"] != "GDHT":
             return
        if data["measurement"] == "temperature":
            humidity = data["value"]
        if data["measurement"] == "humidity":
            temp = data["value"]
        callback(humidity, temp, settings, True)
        #lcd.clear() //OVO MOZDA BUDE POTREBNO
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'Humidity: ' + humidity +'\n' )# display CPU temperature
        lcd.message( 'Temperature: ' + temp )   # display the time

    mqtt_client.on_message = on_message


def run_display_loop(settings, display_callback, stop_event):
    try:
        poject_loop(settings, display_callback, stop_event)
    except KeyboardInterrupt:
        destroy()

        
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

