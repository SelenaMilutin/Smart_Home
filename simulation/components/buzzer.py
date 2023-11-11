from simulators.buzzer import run_buzz_simulation
import threading

def callback(val):
    # t = time.localtime()
    print("BUZZER")
    print("="*20)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Entered pin {pin_val}")
    print(f"Buzzer {val}")

     

def run_buzzer(settings, threads, stop_event):
        # print("!!!!!!!!!!!!!!!!!!!!!!")
        # print("SA SPACE SE PALI A BACSPACE ISKLJUCUJE SLUSANJE ZA TASTATURU ZA SAD")
        if settings['simulated']:
            print("Starting buzz sumilator")
            buzz_thread = threading.Thread(target = run_buzz_simulation, args=(callback, stop_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz sumilator started")
        else:
            from actuators.buzzer import run_buzz_legit
            print("Starting Buzz loop")
            buzz_thread = threading.Thread(target=run_buzz_legit, args=(settings['pin'], stop_event))
            buzz_thread.start()
            threads.append(buzz_thread)
            print("Buzz loop started")
