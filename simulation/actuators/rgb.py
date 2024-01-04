import time


def turnOff():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def white():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def red():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def green():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def blue():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def yellow():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def purple():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def lightBlue():
    import RPi.GPIO as GPIO
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

RED_PIN = 12
GREEN_PIN = 13
BLUE_PIN = 19

color_functions = {
    2: green,
    3: blue,
    4: yellow,
    5: purple,
    6: lightBlue,
    7: white,
    8: red,
}

def run_light_loop(settings, callback, stop_event, publish_event):
    # """
    #     Toggles on/off and changes light value based on settings.
    #     Settings are updated in component by receiving mqtt message.
    # """
    global RED_PIN, GREEN_PIN, BLUE_PIN
    import RPi.GPIO as GPIO
    RED_PIN = settings['pin-r']
    GREEN_PIN = settings['pin-g']
    BLUE_PIN = settings['pin-b']
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin-r'], GPIO.OUT)
    GPIO.setup(settings['pin-g'], GPIO.OUT)
    GPIO.setup(settings['pin-b'], GPIO.OUT)
    while True:
        if settings['on'] == 1:
            selected_color = int(settings["val"])
            color_functions[selected_color]()
        else: 
            turnOff()
        callback(settings["val"], settings["on"], settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(1)  
