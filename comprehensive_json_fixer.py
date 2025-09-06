#!/usr/bin/env python3
import json
import glob
import os
import re

def fix_comprehensive_json_issues(file_path):
    """Comprehensively fix all JSON issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changes_made = False
        
        def process_item(item):
            nonlocal changes_made
            if isinstance(item, dict):
                for key, value in item.items():
                    if key == "question_text" and isinstance(value, str):
                        original = value
                        
                        # Fix all underscore patterns
                        # Pattern 1: \\_\\_ -> = _
                        value = re.sub(r'\\\\_\\\\_', '= _', value)
                        
                        # Pattern 2: \\_ -> = _
                        value = re.sub(r'\\\\_', '= _', value)
                        
                        # Pattern 3: __ (double underscore) -> = _
                        value = re.sub(r'__+', '= _', value)
                        
                        # Pattern 4: Single trailing underscore after period/newline
                        value = re.sub(r'(\.\s*\n\s*)_+\s*$', r'\1= _', value)
                        value = re.sub(r'(\.\s*)_+\s*$', r'\1= _', value)
                        
                        # Pattern 5: Standalone underscore at end
                        value = re.sub(r'\b_+\s*$', '= _', value)
                        
                        # Pattern 6: Multiple underscores
                        value = re.sub(r'_{2,}', '= _', value)
                        
                        # Pattern 7: Fix spacing around equals
                        value = re.sub(r'=\s*_+', '= _', value)
                        
                        # Pattern 8: Remove multiple spaces
                        value = re.sub(r'\s{2,}', ' ', value)
                        
                        # Ensure proper ending
                        if not value.strip().endswith('= _'):
                            if value.strip().endswith('_'):
                                value = re.sub(r'_\s*$', '= _', value.strip())
                            elif not value.strip().endswith('.'):
                                value = value.strip() + '\n= _'
                        
                        if value != original:
                            item[key] = value
                            changes_made = True
                            print(f"Fixed question_text in {file_path}")
                    
                    elif isinstance(value, (dict, list)):
                        process_item(value)
            elif isinstance(item, list):
                for sub_item in item:
                    process_item(sub_item)
        
        process_item(data)
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {file_path}")
        
        return changes_made
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Find all Gr6_*_variations.json files
    json_files = glob.glob("Gr6_*_variations.json")
    
    total_files = len(json_files)
    fixed_files = 0
    
    print(f"Found {total_files} JSON files to process")
    
    for file_path in sorted(json_files):
        print(f"\nProcessing {file_path}...")
        if fix_comprehensive_json_issues(file_path):
            fixed_files += 1
    
    print(f"\nCompleted! Fixed {fixed_files} out of {total_files} files")

if __name__ == "__main__":
    main()