import time
import random

from simulation.alarm.alarm import activate_alarm


def generate_values():
      while True:
            rnd = random.randint(0, 1)
            
            yield rnd
      

def run_ds_simulator(settings, callback, stop_event, publish_event):
    previous = 0
    counter = 0
    alarm_activated = False
    while True:
        pressed = random.randint(0, 1)
        # pressed button
        if (pressed==1 and previous==0):
            callback(settings, publish_event, True)
        elif (pressed == 1 and previous ==1):
            counter += 1
            callback(settings, publish_event)
        # holding button pressed
        elif (pressed == 1 and previous ==1):
             counter += 1
             print(counter)
        # reliesed button
        elif (pressed==0 and previous==1):
            counter = 0
            if alarm_activated:
                alarm_activated = False
                activate_alarm("deactivate", settings["simulated"], settings["name"], settings["runs_on"])

        if counter >= 4:
            activate_alarm("activate", settings["simulated"], settings["name"], settings["runs_on"], True)
        previous = pressed
        time.sleep(1)
        if stop_event.is_set():
            break
              