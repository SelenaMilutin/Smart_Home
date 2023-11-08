def turn_on_off(actuator_settings, on_off):
    
    if (not actuator_settings['simulated']):
        import RPi.GPIO as GPIO
        import time
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(actuator_settings['pin'], GPIO.OUT)
        if on_off == 'on': GPIO.output(actuator_settings['pin'], GPIO.HIGH)
        elif on_off == 'off': GPIO.output(actuator_settings['pin'], GPIO.LOW)
        time.sleep(1)
    else:
        status = True if on_off == 'on' else False if on_off == 'off' else None
        if status != None:
            print(f"Light has become {on_off}")