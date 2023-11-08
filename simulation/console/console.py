
import threading

from actuators.light import turn_on_off


def parse_input(input_string):
    input_parts = input_string.split(', ')
    actuator_name = None
    command = None

    for part in input_parts:
        if part.startswith('act='):
            actuator_name = part.split('=')[1]
        elif part.startswith('com='):
            command = part.split('=')[1]

    if actuator_name is None or command is None:
        raise ValueError("Invalid input format. Please provide 'act' and 'com' values.")

    if command not in ['on', 'off']:
        raise ValueError("Invalid command. Please provide 'on' or 'off'.")

    return actuator_name, command

def get_input(settings, callback, stop_event):
    
    while True:

        print("Enter input in the format 'act={actuator_name}, com={on/off}'")
        try:
            user_input = input("Enter command: ")
            actuator_name, command = parse_input(user_input)
            print("Command accepted")

            actuators[actuator_name](settings[actuator_name], command)

        except ValueError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f'Key error - actuator not found: {e}')

        if stop_event.is_set():
            break

actuators = {
    'DL': turn_on_off
}

def run_console(settings, threads, stop_event):
    console_thread = threading.Thread(target = get_input, args=(settings, None, stop_event))
    console_thread.start()
    threads.append(console_thread)