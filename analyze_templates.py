import json
import re
from collections import defaultdict

# Read the file content
with open('file.json', 'r') as f:
    content = f.read()

# Split by line and try to detect JSON objects
lines = content.strip().split('\n')
objects = []
current_obj = []
bracket_count = 0
in_object = False

for line in lines:
    # Check if this is the start of a new object
    if line.strip().startswith('{'):
        in_object = True
        current_obj = [line]
        bracket_count = line.count('{') - line.count('}')
    elif in_object:
        current_obj.append(line)
        bracket_count += line.count('{') - line.count('}')
        
        # Check if object is complete
        if bracket_count == 0:
            obj_str = '\n'.join(current_obj)
            # Remove trailing comma if present
            obj_str = obj_str.rstrip(',')
            try:
                obj = json.loads(obj_str)
                objects.append(obj)
            except json.JSONDecodeError as e:
                print(f"Failed to parse object: {e}")
            current_obj = []
            in_object = False

print(f"Total questions found: {len(objects)}")
print()

# Group by tags
tag_groups = defaultdict(list)
for obj in objects:
    if 'tag' in obj:
        tag_groups[obj['tag']].append(obj)

# Analyze each tag
for tag in sorted(tag_groups.keys()):
    questions = tag_groups[tag]
    print(f"\nTag: {tag}")
    print(f"  Total templates: {len(questions)}")
    
    # Check question types
    q_types = set([q.get('question_type', 'Unknown') for q in questions])
    print(f"  Question types: {', '.join(q_types)}")
    
    # Check question numbers
    q_numbers = [q.get('question_number', '') for q in questions]
    print(f"  Question numbers: {', '.join(sorted(q_numbers))}")
    
    # Check for images
    has_images = any('image' in str(q) for q in questions)
    print(f"  Has images: {has_images}")
    
    # Skills
    skills = set([q.get('skills', '') for q in questions if q.get('skills')])
    if skills:
        print(f"  Skills: {', '.join(skills)}")

# Save parsed templates for easier processing
with open('parsed_templates.json', 'w') as f:
    json.dump(tag_groups, f, indent=2)

print(f"\nParsed templates saved to parsed_templates.json")
print(f"\nVariations needed per tag: {51 - len(questions)} variations (to reach 51 total)")