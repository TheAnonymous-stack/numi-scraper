import json
import glob
import os

def fix_json_formatting(filepath):
    """
    Reformat JSON to have opening bracket on new line after "quizzes":
    """
    try:
        # Read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to formatted string with custom formatting
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Replace the pattern to put [ on new line
        json_str = json_str.replace('"quizzes": [', '"quizzes":\n[')
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        return True
            
    except Exception as e:
        print(f"[ERROR] {os.path.basename(filepath)}: {e}")
        return False

def main():
    # Find all Grade 6 JSON files
    pattern = r"C:\Users\kapil\numi-scraper\Gr6_*_E*_variations.json"
    json_files = glob.glob(pattern)
    
    print(f"Fixing formatting for {len(json_files)} files...")
    
    success = 0
    for filepath in json_files:
        if fix_json_formatting(filepath):
            success += 1
    
    print(f"Done! Fixed {success}/{len(json_files)} files")

if __name__ == "__main__":
    main()