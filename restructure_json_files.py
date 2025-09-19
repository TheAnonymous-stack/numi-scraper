import json
import os
import glob

def restructure_json_file(file_path):
    """Restructure a JSON file to have all questions under a 'quizzes' array."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if it's already in the correct format
        if isinstance(data, dict) and 'quizzes' in data:
            print(f"[OK] {os.path.basename(file_path)} - already has quizzes structure")
            return True

        # If it's a list, wrap it in quizzes
        if isinstance(data, list):
            new_structure = {"quizzes": data}

            # Write back the restructured data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_structure, f, indent=2, ensure_ascii=False)

            print(f"[DONE] {os.path.basename(file_path)} - restructured successfully ({len(data)} questions)")
            return True

        # If it's a single object (not a list), wrap it in a quizzes array
        elif isinstance(data, dict) and 'quizzes' not in data:
            new_structure = {"quizzes": [data]}

            # Write back the restructured data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_structure, f, indent=2, ensure_ascii=False)

            print(f"[DONE] {os.path.basename(file_path)} - restructured successfully (1 question)")
            return True

    except json.JSONDecodeError as e:
        print(f"[ERROR] {os.path.basename(file_path)} - JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {os.path.basename(file_path)} - Error: {e}")
        return False

def main():
    """Find and restructure all variation JSON files."""

    # Pattern to find all variation JSON files
    variation_patterns = [
        "Gr7_*_variations.json",
        "Gr7_* variations.json",  # Files with spaces
        "*_variations.json"
    ]

    all_json_files = set()

    # Find all matching JSON files
    for pattern in variation_patterns:
        files = glob.glob(pattern)
        all_json_files.update(files)

    # Also check for the main files
    main_files = ["file.json", "test.json", "file_fixed.json", "test_fixed.json"]
    for file in main_files:
        if os.path.exists(file):
            all_json_files.add(file)

    if not all_json_files:
        print("No JSON files found to restructure.")
        return

    print(f"\nFound {len(all_json_files)} JSON files to process\n")
    print("=" * 60)

    successful = 0
    failed = 0

    # Sort files for consistent output
    for file_path in sorted(all_json_files):
        if restructure_json_file(file_path):
            successful += 1
        else:
            failed += 1

    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Successfully restructured: {successful} files")
    if failed > 0:
        print(f"  Failed: {failed} files")

    # Verify a sample file
    if successful > 0:
        sample_file = sorted(all_json_files)[0]
        print(f"\nVerifying structure of {os.path.basename(sample_file)}:")
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'quizzes' in data:
                print(f"  [OK] Has 'quizzes' key")
                print(f"  [OK] Contains {len(data['quizzes'])} questions")
                if len(data['quizzes']) > 0:
                    first_question = data['quizzes'][0]
                    print(f"  [OK] First question tag: {first_question.get('tag', 'N/A')}")

if __name__ == "__main__":
    main()