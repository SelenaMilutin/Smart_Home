import datetime
import time
# from pynput import keyboard

# def ctrl(letter): return chr(ord(letter.upper())-64)



# def on_press_real(port, settings, key, callback, publish_event):
#     import RPi.GPIO as GPIO

#     if key == keyboard.Key.space:
#         # print("jsjs")
#         try:
#             pitch = 440
#             duration = 0.1
#             period = 1.0 / pitch
#             delay = period / 2
#             cycles = int(duration * pitch)
#             for i in range(cycles):
#                 GPIO.output(port, True)
#                 time.sleep(delay)
#                 GPIO.output(port, False)
#                 time.sleep(delay)
#             print("Buzzzz")
#             callback(1, settings, publish_event)
#         except IOError:
#             print("Error")
    
# def on_release_real(port, settings, key, callback, publish_event):
#     print(port)
#     if key == keyboard.Key.space:
#         print("No more buzz")
#         callback(0, settings, publish_event)
#     if key == keyboard.Key.ctrl_l:
#         keyboard.Listener.stop
#         print("ugasena je tastatura")
#         return False

        
def run_buzz_legit(settings, stop_event, publish_event, callback):
    port = settings['pin']
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)

    pitch = 440
    duration = 0.1
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)

    while True:
        if settings['on']:
            try:
                for i in range(cycles):
                    GPIO.output(port, True)
                    time.sleep(delay)
                    GPIO.output(port, False)
                    time.sleep(delay)
                print("Buzzzz")
                callback(1, settings, publish_event)
            except IOError:
                print("Error")
        else: 
            callback(0, settings, publish_event)
        
        if settings['name'] == 'BB':
            if settings['clock']['hour'] != -1: # clock is set
                t = datetime.now()
                if t.hour == settings['clock']['hour'] and t.minute == settings['clock']['minute']: # clock sounds off at set time
                    settings['on'] = True  

        if stop_event.is_set():
            break
        time.sleep(0.1)  
    # with keyboard.Listener(on_press=partial(on_press_real, port, settings,callback, publish_event), on_release=partial(on_release_real, port, settings, callback, publish_event)) as listener:
    #     listener.join()