import threading

from simulators.dus import run_dus_simulator


def dus_callback(val):
    # t = time.localtime()
    # print("DOOR ULTRASONIC SENSOR")
    # print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Distance: {val}")


def run_dus(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dus simulator")
            dus_thread = threading.Thread(target = run_dus_simulator, args=(settings, dus_callback, stop_event))
            dus_thread.start()
            threads.append(dus_thread)
            print("dus simulator started")
        else:
            from sensors.dus import run_dus_loop
            print("Starting dus loop")
            dus_thread = threading.Thread(target=run_dus_loop, args=(settings, dus_callback, stop_event))
            dus_thread.start()
            threads.append(dus_thread)
            print("dus loop started")
