import json

def load_settings(filePath='settings.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
    

def save_settings(data, filePath='house_info.json'):
    with open(filePath, 'w') as f:
        f.write(json.dumps(data))