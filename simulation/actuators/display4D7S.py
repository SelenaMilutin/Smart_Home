import time

# GPIO ports for the 7seg pins
# segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
# GPIO ports for the digit 0-3 pins 
# digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}

def run_display_loop(settings, callback, stop_event):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    segments = settings["segments"]
    digits = settings["digits"]

    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)
    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)
    
    try:
        while True:

            start_time = time.time() 
            elapsed_time = 0.0

            if settings['clock']['hour'] != -1: # clock is set
                if int(time.ctime()[11:13]) == settings['clock']['hour'] and int(time.ctime()[14:16]) == settings['clock']['minute']: # clock sounds off at set time
                    settings['blink'] = True   

            while elapsed_time < 0.5:  # display for 0.5 seconds
                n = time.ctime()[11:13]+time.ctime()[14:16]
                s = str(n).rjust(4)
                for digit in range(4):
                    for loop in range(0,7):
                        GPIO.output(segments[loop], num[s[digit]][loop])
                        if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                            GPIO.output(25, 1)
                        else:
                            GPIO.output(25, 0)
                    GPIO.output(digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(digits[digit], 1)
                elapsed_time = time.time() - start_time

            if settings['blink']: # hide display for 0.5 seconds to achieve blinking
                time.sleep(0.5)
    finally:
        GPIO.cleanup()
    
              