

from simulators.dms import run_dms_simulator
import threading
from server.messenger_sender import send_measurement


def callback(pin_val, settings):
    # t = time.localtime()
    print("DOOR MEMBRANE SWITCH")
    print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Entered pin {pin_val}")
    if (pin_val == 1):
        print(f"Activated")
        send_measurement(pin_val, settings)


def run_dms(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dms simulator")
            dms_thread = threading.Thread(target = run_dms_simulator, args=(settings, callback, stop_event))
            dms_thread.start()
            threads.append(dms_thread)
            print("dms simulator started")
        else:
            from sensors.dms import run_dms_loop
            print("Starting dms loop")
            dms_thread = threading.Thread(target=run_dms_loop, args=(settings, callback, stop_event))
            dms_thread.start()
            threads.append(dms_thread)
            print("dms loop started")
