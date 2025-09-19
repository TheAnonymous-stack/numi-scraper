import json

# Read the file
with open('test.json', 'r') as f:
    content = f.read()

# Remove trailing comma if present
content = content.rstrip()
if content.endswith(','):
    content = content[:-1]

# Wrap in array brackets
content = '[' + content + ']'

# Parse to validate and pretty-print
try:
    data = json.loads(content)
    print(f"Successfully parsed {len(data)} items")

    # Save the fixed JSON
    with open('test_fixed.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved fixed JSON to test_fixed.json")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    # Try to save the partially fixed content anyway
    with open('test_fixed.json', 'w') as f:
        f.write(content)