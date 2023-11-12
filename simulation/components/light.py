

from simulators.light import run_light_simulator
import threading

def callback(val):
    # t = time.localtime()
    print("LIGHT")
    print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Entered pin {pin_val}")
    print(f"Light {val}")


def run_light(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting light simulator")
            light_thread = threading.Thread(target = run_light_simulator, args=(callback, stop_event))
            light_thread.start()
            threads.append(light_thread)
            print("light simulator started")
        else:
            from actuators.light import run_light_loop
            print("Starting light loop")
            light_thread = threading.Thread(target=run_light_loop, args=(settings, callback, stop_event))
            light_thread.start()
            threads.append(light_thread)
            print("light loop started")
