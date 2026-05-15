import json

def write_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)