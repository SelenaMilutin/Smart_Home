import time      

def run_display_simulator(settings, callback, stop_event):
      while True:
            current_timestamp = time.localtime()
            callback(current_timestamp, settings, True)
            if stop_event.is_set():
                  break
            time.sleep(10)
      
              