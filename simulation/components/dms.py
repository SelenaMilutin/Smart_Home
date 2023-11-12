

from simulators.dms import run_dms_simulator
import threading

def callback(pin_val):
    # t = time.localtime()
    print("DOOR MEMBRANE SWITCH")
    print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Entered pin {pin_val}")
    print(f"Activated")


def run_dms(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dms simulator")
            dms_thread = threading.Thread(target = run_dms_simulator, args=(callback, stop_event))
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
