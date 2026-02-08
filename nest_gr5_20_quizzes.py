import json

# Process all three Gr5_20 files
files_to_process = [
    "Gr5_20_E1_variations.json",
    "Gr5_20_E2_variations.json",
    "Gr5_20_E3_variations.json"
]

for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if it's already nested under "quizzes"
        if isinstance(data, list):
            # Wrap it in a "quizzes" key
            nested_data = {"quizzes": data}

            # Write back to the file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(nested_data, f, indent=2, ensure_ascii=False)

            print(f"Updated: {filename} ({len(data)} questions nested under 'quizzes')")
        elif isinstance(data, dict) and "quizzes" in data:
            print(f"Already nested: {filename}")
        else:
            print(f"Unexpected format: {filename}")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll Gr5_20 files updated!")
