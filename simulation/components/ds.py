

from simulators.ds import run_ds_simulator
import threading
import time

def callback(event):
    # t = time.localtime()
    print("BUTTON")
    print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Door open")


def run_ds(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting ds1 sumilator")
            ds1_thread = threading.Thread(target = run_ds_simulator, args=(callback, stop_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Ds1 sumilator started")
        else:
            from sensors.ds import run_ds_loop
            print("Starting ds1 loop")
            ds1_thread = threading.Thread(target=run_ds_loop, args=(settings['pin'], callback, stop_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Ds1 loop started")
