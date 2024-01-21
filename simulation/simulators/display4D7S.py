import datetime
import time      

def run_display_simulator(settings, callback, stop_event):
      while True:
            if settings['clock']['hour'] != -1: # clock is set
                t = datetime.now()
                if t.hour == settings['clock']['hour'] and t.minute == settings['clock']['minute']: # clock sounds off at set time
                    settings['blink'] = True   
            current_timestamp = time.localtime()
            callback(current_timestamp, settings, True)
            if stop_event.is_set():
                  break
            time.sleep(10)
      
              