import RPi.GPIO as GPIO
import time


def readLine(line, characters, c_tuple):
    char = ""
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(c_tuple[0]) == 1):
        print(characters[0])
        char = characters[0]
    if(GPIO.input(c_tuple[1]) == 1):
        print(characters[1])
        char = characters[1]
    if(GPIO.input(c_tuple[2]) == 1):
        print(characters[2])
        char = characters[2]
    if(GPIO.input(c_tuple[3]) == 1):
        print(characters[3])
        char = characters[3]
    GPIO.output(line, GPIO.LOW)
    return char

def run_dms_loop(settings, callback, stop_event, publish_event):

    R1 = settings['R1']
    R2 = settings['R2']
    R3 = settings['R3']
    R4 = settings['R4']

    C1 = settings['C1']
    C2 = settings['C2']
    C3 = settings['C3']
    C4 = settings['C4']
    c_tuple = (C1, C2, C3, C4)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)


    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    pin = ""
    while True:
        pin += readLine(R1, ["1","2","3","A"], c_tuple)
        pin += readLine(R2, ["4","5","6","B"], c_tuple)
        pin += readLine(R3, ["7","8","9","C"], c_tuple)
        last = readLine(R4, ["*","0","#","D"], c_tuple)
        if last == "0":
            pin += last
        if last == "#": # Terminating key, pin is entered
            callback(pin, settings, publish_event, True)
            pin = ""
        time.sleep(0.2)

        if stop_event.is_set():
            return
