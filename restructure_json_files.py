import json
import os
from pathlib import Path
import glob

def restructure_json_file(filepath):
    """
    Restructure a JSON file to wrap its content in a 'quizzes' key.
    """
    try:
        # Read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if already has the correct structure
        if isinstance(data, dict) and 'quizzes' in data:
            print(f"[OK] Already structured: {os.path.basename(filepath)}")
            return False
        
        # If data is a list, wrap it in quizzes
        if isinstance(data, list):
            new_data = {
                "quizzes": data
            }
            
            # Write back with proper formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            
            print(f"[FIXED] {os.path.basename(filepath)}")
            return True
        else:
            print(f"[WARNING] Unexpected structure in: {os.path.basename(filepath)}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON Error in {os.path.basename(filepath)}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error processing {os.path.basename(filepath)}: {e}")
        return False

def main():
    """
    Process all Grade 6 JSON variation files.
    """
    print("=" * 60)
    print("JSON File Restructuring Script")
    print("=" * 60)
    
    # Find all Grade 6 JSON files
    pattern = r"C:\Users\kapil\numi-scraper\Gr6_*_E*_variations.json"
    json_files = glob.glob(pattern)
    
    if not json_files:
        print("No Grade 6 JSON files found!")
        return
    
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    print("-" * 60)
    
    fixed_count = 0
    already_correct = 0
    error_count = 0
    
    for filepath in sorted(json_files):
        result = restructure_json_file(filepath)
        if result is True:
            fixed_count += 1
        elif result is False:
            # Check if it was already correct
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'quizzes' in data:
                    already_correct += 1
                else:
                    error_count += 1
    
    print("-" * 60)
    print(f"\nProcessing Complete!")
    print(f"Files fixed: {fixed_count}")
    print(f"Already correct: {already_correct}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {len(json_files)}")
    
    # Also check Gr6_1_E1_variations.json specifically since it was mentioned
    gr6_1_e1_path = r"C:\Users\kapil\numi-scraper\Gr6_1_E1_variations.json"
    if os.path.exists(gr6_1_e1_path):
        print(f"\nChecking Gr6_1_E1_variations.json specifically...")
        with open(gr6_1_e1_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'quizzes' in data:
                print("[OK] Gr6_1_E1_variations.json already has correct structure")
            else:
                print("[INFO] Gr6_1_E1_variations.json needs restructuring")
                restructure_json_file(gr6_1_e1_path)

if __name__ == "__main__":
    main()