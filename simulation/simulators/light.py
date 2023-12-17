# import keyboard
import time

# def on_key_event_wrapper(callback):
#     """
#         Sets keyboard hook to register 'l' to turn light on and off.
#     """
#     on_off = 'off'
#     def on_key_event(event):
#         nonlocal on_off
#         if event.event_type == keyboard.KEY_DOWN and event.name == 'l':
#             on_off = 'off' if on_off == 'on' else 'on' if on_off == 'off' else on_off
#             callback(on_off)            
#             time.sleep(0.1)

#     return on_key_event

def run_light_simulator(callback, stop_event):
    # keyboard.hook(on_key_event_wrapper(callback))
    while True:
        if stop_event.is_set():
            break
        time.sleep(1)