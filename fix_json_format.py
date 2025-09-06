import json
import re

# Read the file content
with open('file.json', 'r') as f:
    content = f.read()

# Split by line and look for JSON objects
lines = content.strip().split('\n')

# Build proper JSON array
json_objects = []
current_obj = ""
brace_count = 0

for line in lines:
    current_obj += line + "\n"
    brace_count += line.count('{') - line.count('}')
    
    if brace_count == 0 and current_obj.strip():
        # We have a complete object
        try:
            obj = json.loads(current_obj.strip().rstrip(','))
            json_objects.append(obj)
            current_obj = ""
        except:
            # Continue if not a complete object
            pass

# Save as proper JSON array
with open('file_fixed.json', 'w') as f:
    json.dump(json_objects, f, indent=2)

# Analyze the data
tags = set([q['tag'] for q in json_objects if 'tag' in q])
print('Unique tags found:', sorted(tags))
print('Number of unique tags:', len(tags))

# Count templates per tag
for tag in sorted(tags):
    count = len([q for q in json_objects if q.get('tag') == tag])
    print(f'{tag}: {count} template(s)')