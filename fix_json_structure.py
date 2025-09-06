import json
import re

# Read the file
with open('file.json', 'r') as f:
    content = f.read()

# Split by the pattern that separates JSON objects
objects = []
current = ''
depth = 0
in_string = False
escape_next = False

for char in content:
    if escape_next:
        current += char
        escape_next = False
        continue
    
    if char == '\\' and in_string:
        escape_next = True
        current += char
        continue
    
    if char == '"' and not escape_next:
        in_string = not in_string
    
    if not in_string:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            
    current += char
    
    if depth == 0 and current.strip() and current.strip().endswith('}'):
        try:
            obj = json.loads(current.strip())
            objects.append(obj)
            current = ''
        except Exception as e:
            pass

# Save as proper JSON array
with open('parsed_templates.json', 'w') as f:
    json.dump(objects, f, indent=2)

print(f'Successfully parsed {len(objects)} questions')

# Get unique tags
tags = set(obj.get('tag', '') for obj in objects if 'tag' in obj)
print(f'Unique tags: {sorted(tags)}')

# Count questions per tag
from collections import Counter
tag_counts = Counter(obj.get('tag', '') for obj in objects if 'tag' in obj)
for tag, count in sorted(tag_counts.items()):
    print(f'{tag}: {count} template(s)')