import json
import re

# Read the raw content
with open('file2.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Manually parse by finding each complete JSON object
# We'll look for the pattern of opening and closing braces at the same level
def extract_json_objects(text):
    objects = []
    brace_count = 0
    current_obj = ""
    in_string = False
    escape_next = False
    
    for char in text:
        if escape_next:
            current_obj += char
            escape_next = False
            continue
            
        if char == '\\' and in_string:
            escape_next = True
            current_obj += char
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            
        if not in_string:
            if char == '{':
                if brace_count == 0:
                    current_obj = ""
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                
        current_obj += char
        
        if brace_count == 0 and current_obj.strip() and current_obj.strip().endswith('}'):
            # We have a complete object
            try:
                obj_str = current_obj.strip().strip(',')
                obj = json.loads(obj_str)
                objects.append(obj)
                current_obj = ""
            except Exception as e:
                print(f"Failed to parse object: {e}")
                print(f"Object starts with: {obj_str[:100]}")
    
    return objects

# Extract objects
questions = extract_json_objects(content)

print(f"Extracted {len(questions)} questions")

# Analyze tags
tags = {}
for q in questions:
    tag = q.get('tag', 'NO_TAG')
    if tag not in tags:
        tags[tag] = []
    tags[tag].append(q)

print("\nUnique tags found:")
for tag in sorted(tags.keys()):
    template_numbers = [q.get('question_number', '1_1') for q in tags[tag]]
    print(f"  {tag}: {len(tags[tag])} templates (question_numbers: {template_numbers})")

# Save the properly formatted JSON
with open('templates.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2)
    
print(f"\nSaved {len(questions)} questions to templates.json")