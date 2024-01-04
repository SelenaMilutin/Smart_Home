import threading
import time

from simulation.simulators.display4D7S import run_display_simulator


def display_callback(timestamp, display_settings, verbose=False):

    if verbose:
        t = time.localtime()
        print("="*20)
        print("4D7S display")
        print(f"Timestamp: {time.strftime('%H:%M', timestamp)}")


def run_4D7Sdisplay(settings, threads, stop_event):
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