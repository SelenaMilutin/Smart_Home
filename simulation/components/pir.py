

from simulators.pir import run_pir_simulator
import threading
import time
from server.messenger_sender import send_measurement


def callback_room_pir(settings):
    # t = time.localtime()
    # print("ROOM PASSIVE INFRARED SENSOR")
    # print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Motion detected in room")
    send_measurement(1, settings)


def callback_door_pir(settings):
    # t = time.localtime()
    # print("DOOR PASSIVE INFRARED SENSOR")
    # print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Motion detected at door")
    send_measurement(1, settings)


def run_pir(settings, threads, stop_event, location):
        if settings['simulated']:
            print("Starting ds1 sumilator")
            if location == "room":
                rpir_thread = threading.Thread(target = run_pir_simulator, args=(settings, callback_room_pir, stop_event))
            else:
                rpir_thread = threading.Thread(target = run_pir_simulator, args=(settings, callback_door_pir, stop_event))
            rpir_thread.start()
            threads.append(rpir_thread)
            print("Rpir1 sumilator started")
        else:
            from sensors.pir import run_pir_loop
            print("Starting rpir1 loop")
            if location == "room":
                rpir_thread = threading.Thread(target=run_pir_loop, args=(settings['pin'], callback_room_pir, location, stop_event))
            else:
                rpir_thread = threading.Thread(target=run_pir_loop, args=(settings['pin'], callback_door_pir, location, stop_event))
            rpir_thread.start()
            threads.append(rpir_thread)
            print("Rpir1 loop started")
