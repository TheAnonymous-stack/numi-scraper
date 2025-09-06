import json
import glob
import os

def fix_tags_in_file(filepath):
    """Fix tag format in a single variation file."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract base tag from filename
        filename = os.path.basename(filepath)
        # Remove _variations.json to get base tag like Gr6_1_E1
        base_tag = filename.replace('_variations.json', '')
        
        # Fix tags for each variation
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict) and 'tag' in item:
                    # Update tag to include variation number
                    item['tag'] = f"{base_tag}_V{i}"
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True, f"Fixed {len(data)} variations"
    
    except Exception as e:
        return False, str(e)

def main():
    # Find all Grade 6 variation files
    pattern = 'Gr6_*_E*_variations.json'
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} Grade 6 variation files to fix")
    print("="*60)
    
    success_count = 0
    error_count = 0
    errors = []
    
    for filepath in sorted(files):
        success, message = fix_tags_in_file(filepath)
        
        if success:
            success_count += 1
            print(f"[OK] {os.path.basename(filepath)}: {message}")
        else:
            error_count += 1
            errors.append((filepath, message))
            print(f"[ERROR] {os.path.basename(filepath)}: {message}")
    
    print("="*60)
    print(f"\nSummary:")
    print(f"  Successfully fixed: {success_count} files")
    print(f"  Errors: {error_count} files")
    
    if errors:
        print("\nError details:")
        for filepath, error in errors:
            print(f"  - {os.path.basename(filepath)}: {error}")
    
    print(f"\nTag format fix complete!")
    return success_count, error_count

if __name__ == "__main__":
    success, errors = main()