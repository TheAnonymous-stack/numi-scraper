def write_to_json(data, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)