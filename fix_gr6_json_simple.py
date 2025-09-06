import json
import os
import re
import glob
from typing import Dict, List, Any

def fix_underscore_patterns(text: str) -> str:
    """Fix \\_\\_ patterns in text by replacing them with proper blanks"""
    if not text:
        return text
    
    # Replace various forms of escaped underscores
    text = text.replace('\\_\\_', '_')
    text = text.replace('\\\\__', '_')
    text = text.replace('\\__', '_')
    
    return text

def remove_unnecessary_html(text: str) -> str:
    """Remove unnecessary HTML tags while preserving essential formatting"""
    if not text:
        return text
    
    # Remove specific problematic HTML patterns but keep math formatting
    # Remove div tags but keep content
    text = re.sub(r'<div[^>]*>', '', text)
    text = re.sub(r'</div>', '', text)
    
    # Remove span tags but keep content  
    text = re.sub(r'<span[^>]*>', '', text)
    text = re.sub(r'</span>', '', text)
    
    # Remove p tags but keep content
    text = re.sub(r'<p[^>]*>', '', text)
    text = re.sub(r'</p>', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def process_json_recursively(obj):
    """Recursively process all strings in a JSON object"""
    if isinstance(obj, dict):
        return {key: process_json_recursively(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [process_json_recursively(item) for item in obj]
    elif isinstance(obj, str):
        # Apply both fixes
        obj = fix_underscore_patterns(obj)
        obj = remove_unnecessary_html(obj)
        return obj
    else:
        return obj

def main():
    """Main function to fix all Grade 6 JSON files"""
    # Get all Grade 6 JSON files
    json_files = glob.glob("Gr6_*_variations.json")
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    
    fixed_count = 0
    error_count = 0
    
    for json_file in json_files:
        try:
            print(f"Processing: {json_file}")
            
            # Read JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Process the data
            original_str = json.dumps(data)
            fixed_data = process_json_recursively(data)
            fixed_str = json.dumps(fixed_data)
            
            # Check if changes were made
            if original_str != fixed_str:
                # Create backup
                backup_file = json_file + '.backup'
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Write fixed data
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(fixed_data, f, indent=2, ensure_ascii=False)
                
                print(f"  -> Fixed {json_file}")
                fixed_count += 1
            else:
                print(f"  -> No changes needed for {json_file}")
                
        except Exception as e:
            print(f"  -> ERROR processing {json_file}: {e}")
            error_count += 1
    
    print(f"\nSUMMARY:")
    print(f"Files fixed: {fixed_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {len(json_files)}")

if __name__ == "__main__":
    main()