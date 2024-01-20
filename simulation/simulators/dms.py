import copy
import time
import random
# import keyboard



# def on_key_event_wrapper(callback):
#     """
#         Sets keyboard hook to register '0'-'9' inputs and '#' to finish entering PIN.
#     """
#     pin = ''
#     def on_key_event(event):
#         nonlocal pin
#         if event.event_type == keyboard.KEY_DOWN and event.name.isdigit():
#             print(f"Key '{event.name}' is pressed in simulator")
            # send_measurement(key ili sta vec, settings)

#             pin += event.name
#             time.sleep(0.1)
#         if event.event_type == keyboard.KEY_DOWN and event.name == '#':
#             pin_copy = copy.deepcopy(pin)
#             pin = '' # reset pin value
#             callback(pin_copy)

#     return on_key_event

def generate_values(settings):
    while True:
        pin = ""
        for i in range(4):
            rnd = random.randint(0, 9)
            pin += str(rnd)
            time.sleep(1)
        if (random.randint(1, 10) == 2):  # 10% chance that correct pin is entered
            pin = settings['pin']
        yield pin

def run_dms_simulator(settings, callback, stop_event, publish_event):
    
    # keyboard.hook(on_key_event_wrapper(callback))
    # while True:
    #     if stop_event.is_set():
    #         break
    #     time.sleep(1)

    for val in generate_values(settings):
        callback(val, settings, publish_event, True)
        if stop_event.is_set():
            break
        time.sleep(5)

   
              