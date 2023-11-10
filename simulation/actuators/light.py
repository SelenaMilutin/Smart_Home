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

def run_light_loop(settings, callback, stop_event):
    """
        Sets light to on or off depending on settings.json.
        In loop starts callback every 10 seconds reporting light status (on or off).
    """
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.OUT)
    on_off = GPIO.HIGH if settings['on'] else GPIO.LOW
    GPIO.output(settings['pin'], on_off)
    while True:
        callback('on' if GPIO.input(settings['pin']) == GPIO.HIGH else 'off')
        time.sleep(10)  
        if stop_event.is_set():
            break