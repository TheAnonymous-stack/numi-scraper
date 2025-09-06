import json
import re

def parse_json_objects_from_file(filename):
    """Parse a file containing multiple JSON objects separated by commas."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The file appears to have JSON objects separated by },\n{
    # We need to properly parse this
    questions = []
    
    # Remove trailing comma if present
    content = content.strip()
    if content.endswith(','):
        content = content[:-1]
    
    # Add brackets to make it a proper JSON array
    if not content.startswith('['):
        content = '[' + content
    if not content.endswith(']'):
        content = content + ']'
    
    try:
        questions = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        # Try alternative parsing method
        content = content.strip()
        if content.startswith('['):
            content = content[1:]
        if content.endswith(']'):
            content = content[:-1]
        
        # Split by object boundaries
        objects = []
        current = ""
        depth = 0
        in_string = False
        escape_next = False
        
        for char in content:
            if escape_next:
                current += char
                escape_next = False
                continue
            
            if char == '\\':
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
            
            if depth == 0 and current.strip() and char == '}':
                try:
                    obj = json.loads(current.strip().rstrip(','))
                    objects.append(obj)
                    current = ""
                except json.JSONDecodeError as e:
                    print(f"Error parsing object: {e}")
                    print(f"Content: {current[:100]}...")
        
        questions = objects
    
    return questions

# Parse the templates
questions = parse_json_objects_from_file('file2.json')

# Save as proper JSON array
with open('parsed_templates.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

# Analyze tags
tags = {}
for q in questions:
    tag = q.get('tag', 'NO_TAG')
    if tag not in tags:
        tags[tag] = []
    tags[tag].append(q)

print(f"Total questions parsed: {len(questions)}")
print(f"Unique tags found: {len(tags)}")
print("\nTag distribution:")
for tag in sorted(tags.keys()):
    templates = tags[tag]
    print(f"  {tag}: {len(templates)} template(s)")
    for t in templates:
        print(f"    - Question number: {t.get('question_number', 'N/A')}")

# Save tag analysis
tag_info = {}
for tag, templates in tags.items():
    tag_info[tag] = {
        'count': len(templates),
        'question_numbers': [t.get('question_number', 'N/A') for t in templates],
        'question_types': list(set(t.get('question_type', 'N/A') for t in templates)),
        'skills': list(set(t.get('skills', 'N/A') for t in templates))
    }

with open('tag_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(tag_info, f, indent=2)

print("\nTag analysis saved to tag_analysis.json")
print("Parsed templates saved to parsed_templates.json")