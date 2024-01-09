import threading
import time

from simulation.simulators.lcd import run_display_simulator


def display_callback(hymidity, temp, display_settings, verbose=False):

    if verbose:
        t = time.localtime()
        print("="*20)
        print("LCD display")
        print(f"Hymidity: {hymidity}, Temp: {temp}")


def run_LCDdisplay(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting LCD simulator")
            display_thread = threading.Thread(target = run_display_simulator, args=(settings, display_callback, stop_event))
            display_thread.start()
            threads.append(display_thread)
            print("LCD simulator started")
        else:
            from sensors.lcd.LCD1602 import run_display_loop
            print("Starting LCD loop")
            display_thread = threading.Thread(target=run_display_loop, args=(settings, display_callback, stop_event))
            display_thread.start()
            threads.append(display_thread)
            print("LCD started")