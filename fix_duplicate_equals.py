import json
import glob
import re

def fix_duplicate_equals_patterns(text):
    """Fix duplicate equals patterns in text"""
    if not text:
        return text
    
    # Fix the specific pattern "= _== _" to just "= _"
    text = re.sub(r'= _== _', '= _', text)
    
    # Also fix any other variations of this pattern
    text = re.sub(r'=\s*_\s*=+\s*_', '= _', text)
    
    return text

def process_json_file(filepath):
    """Process a single JSON file to fix duplicate equals patterns"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changes_made = False
        
        def process_item(item):
            nonlocal changes_made
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, str):
                        original = value
                        fixed = fix_duplicate_equals_patterns(value)
                        if original != fixed:
                            item[key] = fixed
                            changes_made = True
                    elif isinstance(value, (list, dict)):
                        process_item(value)
            elif isinstance(item, list):
                for i, sub_item in enumerate(item):
                    if isinstance(sub_item, str):
                        original = sub_item
                        fixed = fix_duplicate_equals_patterns(sub_item)
                        if original != fixed:
                            item[i] = fixed
                            changes_made = True
                    elif isinstance(sub_item, (list, dict)):
                        process_item(sub_item)
        
        process_item(data)
        
        if changes_made:
            # Create backup
            backup_path = filepath + '.equals_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Write fixed file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix duplicate equals patterns in all Grade 6 JSON files"""
    json_files = glob.glob("Gr6_*_variations.json")
    print(f"Processing {len(json_files)} JSON files for duplicate equals patterns...")
    
    fixed_count = 0
    
    for json_file in json_files:
        if process_json_file(json_file):
            print(f"Fixed: {json_file}")
            fixed_count += 1
        else:
            print(f"No changes: {json_file}")
    
    print(f"\nSummary:")
    print(f"Files processed: {len(json_files)}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files with no issues: {len(json_files) - fixed_count}")

if __name__ == "__main__":
    main()