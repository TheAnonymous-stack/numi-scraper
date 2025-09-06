import json
import re

def parse_json_objects(file_path):
    """Parse multiple JSON objects from a file that may not be properly formatted as an array."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to parse as a single JSON array first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
    except:
        pass
    
    # If that fails, try to wrap in array brackets
    try:
        wrapped = '[' + content + ']'
        data = json.loads(wrapped)
        return data
    except:
        pass
    
    # If that also fails, try to find individual JSON objects
    objects = []
    
    # Split by common patterns that indicate object boundaries
    # Look for patterns like "},\n{" or "}\n{"
    parts = re.split(r'}\s*,?\s*{', content)
    
    for i, part in enumerate(parts):
        # Add back the braces we split on
        if i > 0:
            part = '{' + part
        if i < len(parts) - 1:
            part = part + '}'
        
        # Clean up any leading/trailing whitespace or commas
        part = part.strip().strip(',')
        
        if part:
            try:
                obj = json.loads(part)
                objects.append(obj)
            except:
                # Try to fix common issues
                if not part.startswith('{'):
                    part = '{' + part
                if not part.endswith('}'):
                    part = part + '}'
                try:
                    obj = json.loads(part)
                    objects.append(obj)
                except Exception as e:
                    print(f"Failed to parse object {i}: {e}")
                    print(f"First 100 chars: {part[:100]}")
    
    return objects

# Parse the file
questions = parse_json_objects('file2.json')
print(f"Successfully parsed {len(questions)} questions")

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
with open('parsed_templates.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2)
print("\nSaved parsed questions to parsed_templates.json")