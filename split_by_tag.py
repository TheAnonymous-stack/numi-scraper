import json
import os
import re
from collections import defaultdict

# Read the combined edited file
with open('combined_edited.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

# Group questions by tag pattern (e.g., "Gr5_3_E1" -> "Gr5_3")
grouped_questions = defaultdict(list)

for question in all_questions:
    tag = question.get('tag', '')
    # Extract the base tag (e.g., "Gr5_3_E1" -> "Gr5_3")
    match = re.match(r'(Gr\d+_\d+)', tag)
    if match:
        base_tag = match.group(1)
        grouped_questions[base_tag].append(question)
    else:
        # If pattern doesn't match, use the full tag
        grouped_questions[tag].append(question)

# Create folders and write JSON files
output_base_dir = 'edited_by_tag'
os.makedirs(output_base_dir, exist_ok=True)

print(f"Creating folders and JSON files in '{output_base_dir}' directory...\n")

for base_tag, questions in sorted(grouped_questions.items()):
    # Create folder for this tag group
    folder_path = os.path.join(output_base_dir, base_tag)
    os.makedirs(folder_path, exist_ok=True)

    # Write JSON file
    json_filename = f"{base_tag}_edited.json"
    json_filepath = os.path.join(folder_path, json_filename)

    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"Created: {folder_path}\\{json_filename} ({len(questions)} questions)")

print(f"\nTotal tag groups: {len(grouped_questions)}")
print(f"Total questions: {sum(len(q) for q in grouped_questions.values())}")
