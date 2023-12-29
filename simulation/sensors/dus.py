import RPi.GPIO as GPIO
import time



def get_distance(pin_echo, pin_trig):
    GPIO.output(pin_trig, False)
    time.sleep(0.2)
    GPIO.output(pin_trig, True)
    time.sleep(0.00001)
    GPIO.output(pin_trig, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

    iter = 0
    while GPIO.input(pin_echo) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(pin_echo) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300)/2
    return distance


def run_dus_loop(settings, callback, stop_event, publish_event):
    pin_trig =settings['pin_trig']
    pin_echo = settings['pin_echo']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_trig, GPIO.OUT)
    GPIO.setup(pin_echo, GPIO.IN)

    while True:
        val = get_distance(pin_echo, pin_trig)
        callback(val, settings, publish_event)
        if stop_event.is_set():
            return

        time.sleep(1)