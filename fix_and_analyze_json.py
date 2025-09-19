import json
import re

# Read the raw file content
with open(r'C:\Users\kapil\numi-scraper\file.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the JSON structure
# Add opening bracket
fixed_content = '[{' + content

# Remove trailing comma if present and close the JSON
fixed_content = fixed_content.rstrip()
if fixed_content.endswith(','):
    fixed_content = fixed_content[:-1]
fixed_content += ']'

# Try to parse
try:
    data = json.loads(fixed_content)
    print(f"Successfully parsed {len(data)} questions")

    # Analyze tags
    tags_info = {}
    for item in data:
        tag = item.get('tag')
        if tag:
            if tag not in tags_info:
                tags_info[tag] = []
            tags_info[tag].append(item.get('question_number'))

    print("\nUnique tags and their question numbers:")
    for tag in sorted(tags_info.keys()):
        print(f"{tag}: {sorted(tags_info[tag])}")

    # Save the fixed JSON
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("\nFixed JSON saved to file_fixed.json")

except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print(f"Error at position: {e.pos}")
    # Try to show the problematic area
    if e.pos:
        start = max(0, e.pos - 100)
        end = min(len(fixed_content), e.pos + 100)
        print(f"Content around error:\n{fixed_content[start:end]}")