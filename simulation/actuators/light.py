import time
import keyboard

# def turn_on_off(actuator_settings, on_off):
# """
#     Works with console input of command to turn light on/off.
# """
    
#     if (not actuator_settings['simulated']):
#         import RPi.GPIO as GPIO
#         import time
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(actuator_settings['pin'], GPIO.OUT)
#         if on_off == 'on': GPIO.output(actuator_settings['pin'], GPIO.HIGH)
#         elif on_off == 'off': GPIO.output(actuator_settings['pin'], GPIO.LOW)
#         time.sleep(1)
#     else:
#         status = True if on_off == 'on' else False if on_off == 'off' else None
#         if status != None:
#             print(f"Light has become {on_off}")

def on_key_event_wrapper(callback, settings):
    """
        Sets keyboard hook to register 'l' to turn light on and off.
    """
    def on_key_event(event):
        nonlocal settings

        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(settings['pin'], GPIO.OUT)
        high_low = GPIO.HIGH if settings['on'] else GPIO.LOW
        GPIO.output(settings['pin'], high_low)

        if event.event_type == keyboard.KEY_DOWN and event.name == 'l':

            if GPIO.input(settings['pin']) == GPIO.HIGH:
                time.sleep(0.2)
                GPIO.output(settings['pin'], GPIO.LOW)
            if GPIO.input(settings['pin']) == GPIO.LOW:
                time.sleep(0.2)
                GPIO.output(settings['pin'], GPIO.HIGH)
            time.sleep(0.1)
            callback('on' if GPIO.input(settings['pin']) == GPIO.HIGH else 'off')
            time.sleep(1)

    return on_key_event


def run_light_loop(settings, callback, stop_event):
    """
        Initializes light to on/off depending on settings.json.
        Sets keyboard hook to listen to key 'l' press to toggle light.
    """
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.OUT)
    high_low = GPIO.HIGH if settings['on'] else GPIO.LOW
    GPIO.output(settings['pin'], high_low)

    keyboard.hook(on_key_event_wrapper(callback, settings))
    while True:
        if stop_event.is_set():
            break
        time.sleep(1)  