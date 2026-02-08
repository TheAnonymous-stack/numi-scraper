import json
import os

# Process all files in edited_by_tag directory
output_base_dir = 'edited_by_tag'

# Get all subdirectories
for folder_name in os.listdir(output_base_dir):
    folder_path = os.path.join(output_base_dir, folder_name)

    if os.path.isdir(folder_path):
        # Find JSON files in this folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                json_filepath = os.path.join(folder_path, filename)

                # Read the current JSON file
                with open(json_filepath, 'r', encoding='utf-8') as f:
                    questions = json.load(f)

                # Check if it's already nested under "quizzes"
                if isinstance(questions, list):
                    # Wrap it in a "quizzes" key
                    nested_data = {"quizzes": questions}

                    # Write back to the file
                    with open(json_filepath, 'w', encoding='utf-8') as f:
                        json.dump(nested_data, f, indent=2, ensure_ascii=False)

                    print(f"Updated: {json_filepath} ({len(questions)} questions)")
                elif isinstance(questions, dict) and "quizzes" in questions:
                    print(f"Already nested: {json_filepath}")
                else:
                    print(f"Unexpected format: {json_filepath}")

print("\nAll files updated to nest under 'quizzes' key!")
