import json
import re

def parse_multiple_json_objects(file_path):
    """Parse a file containing multiple JSON objects separated by commas."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle file that has JSON objects separated by },\n{
    # Add brackets to make it a valid JSON array
    if not content.strip().startswith('['):
        content = '[' + content + ']'

    # Fix any trailing commas before the closing bracket
    content = re.sub(r',\s*]', ']', content)

    try:
        data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        # Try alternative parsing method
        objects = []
        current = ""
        depth = 0

        for char in content:
            current += char
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and current.strip():
                    try:
                        obj = json.loads(current.strip().rstrip(','))
                        objects.append(obj)
                        current = ""
                    except:
                        pass
        return objects

# Parse the file
questions = parse_multiple_json_objects('file.json')

# Analyze the questions
tags_dict = {}
for q in questions:
    if 'tag' in q:
        tag = q['tag']
        if tag not in tags_dict:
            tags_dict[tag] = []
        tags_dict[tag].append(q)

print(f"Total questions found: {len(questions)}")
print(f"\nUnique tags and their template counts:")
for tag in sorted(tags_dict.keys()):
    print(f"  {tag}: {len(tags_dict[tag])} templates")
    q_nums = [q.get('question_number', 'N/A') for q in tags_dict[tag]]
    print(f"    Question numbers: {', '.join(q_nums)}")

# Save the properly formatted data for easier processing
with open('questions_formatted.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("\nFormatted questions saved to questions_formatted.json")