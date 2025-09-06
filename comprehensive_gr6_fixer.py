import json
import os
import re
import glob
from typing import Dict, List, Any

def fix_underscore_patterns(text: str) -> str:
    """Fix \\_\\_ patterns in text by replacing them with proper blanks"""
    if not text:
        return text
    
    # Replace \\_\\_ with _
    text = text.replace('\\_\\_', '_')
    
    # Also handle cases where it might be escaped differently
    text = text.replace('\\\\__', '_')
    text = text.replace('\\__', '_')
    
    return text

def remove_unnecessary_html(text: str) -> str:
    """Remove unnecessary HTML tags while preserving essential formatting"""
    if not text:
        return text
    
    # Keep essential HTML tags for math and formatting
    essential_tags = ['strong', 'em', 'i', 'b', 'u', 'sup', 'sub', 'br']
    
    # Remove unnecessary HTML tags but preserve content
    # This regex removes HTML tags that are not in the essential list
    def replace_html(match):
        tag = match.group(1).lower()
        if tag in essential_tags or tag.startswith('/'):
            return match.group(0)  # Keep essential tags
        else:
            return ''  # Remove unnecessary tags
    
    text = re.sub(r'<(/?\w+)[^>]*>', replace_html, text)
    
    # Clean up multiple spaces and line breaks
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def fix_json_content(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively fix content in JSON data"""
    if isinstance(data, dict):
        fixed_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Fix underscore patterns
                value = fix_underscore_patterns(value)
                # Remove unnecessary HTML
                value = remove_unnecessary_html(value)
            elif isinstance(value, (dict, list)):
                value = fix_json_content(value)
            fixed_data[key] = value
        return fixed_data
    elif isinstance(data, list):
        return [fix_json_content(item) for item in data]
    elif isinstance(data, str):
        # Fix underscore patterns
        data = fix_underscore_patterns(data)
        # Remove unnecessary HTML
        data = remove_unnecessary_html(data)
        return data
    else:
        return data

def get_all_gr6_json_files() -> List[str]:
    """Get all Grade 6 JSON variation files"""
    return glob.glob("Gr6_*_variations.json")

def fix_html_file_naming():
    """Fix HTML file naming to match JSON files properly"""
    html_files = glob.glob("HTML/*.html")
    
    for html_file in html_files:
        basename = os.path.basename(html_file)
        
        # Fix spacing issues in filenames
        if ' ' in basename:
            # Extract the components and create proper filename
            parts = basename.split(' ')
            if len(parts) >= 2:
                prefix = parts[0]  # e.g., "Gr6_15_E5"
                suffix = parts[1].replace('.html', '')  # e.g., "5_1"
                new_name = f"{prefix}_{suffix}.html"
                new_path = os.path.join("HTML", new_name)
                
                try:
                    os.rename(html_file, new_path)
                    print(f"Renamed: {basename} -> {new_name}")
                except FileExistsError:
                    print(f"Warning: Target file {new_name} already exists")
                except Exception as e:
                    print(f"Error renaming {basename}: {e}")

def validate_json_structure(data: Dict[str, Any]) -> List[str]:
    """Validate JSON structure and return any issues found"""
    issues = []
    
    # Check for remaining \\_\\_ patterns
    data_str = json.dumps(data)
    if '\\_\\_' in data_str:
        issues.append("Still contains \\_\\_ patterns")
    
    # Check for unnecessary HTML tags
    if re.search(r'<(?!/?(?:strong|em|i|b|u|sup|sub|br)\b)[^>]*>', data_str):
        issues.append("Contains unnecessary HTML tags")
    
    # Check required fields
    required_fields = ['skills', 'question_text', 'tag', 'question_number']
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: {field}")
    
    return issues

def main():
    """Main function to fix all Grade 6 JSON files"""
    json_files = get_all_gr6_json_files()
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    
    # Fix HTML file naming first
    print("\nFixing HTML file naming...")
    fix_html_file_naming()
    
    # Process each JSON file
    total_files = len(json_files)
    fixed_files = 0
    error_files = []
    
    for i, json_file in enumerate(json_files, 1):
        print(f"\nProcessing {i}/{total_files}: {json_file}")
        
        try:
            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Fix the content
            original_data_str = json.dumps(data)
            fixed_data = fix_json_content(data)
            fixed_data_str = json.dumps(fixed_data)
            
            # Check if changes were made
            if original_data_str != fixed_data_str:
                # Create backup
                backup_file = json_file + '.backup'
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Write fixed data
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(fixed_data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✓ Fixed and saved {json_file}")
                fixed_files += 1
            else:
                print(f"  - No changes needed for {json_file}")
            
            # Validate the fixed file
            issues = validate_json_structure(fixed_data)
            if issues:
                print(f"  ⚠ Validation issues: {', '.join(issues)}")
        
        except Exception as e:
            print(f"  ✗ Error processing {json_file}: {e}")
            error_files.append(json_file)
    
    # Summary
    print(f"\n" + "="*50)
    print(f"SUMMARY")
    print(f"="*50)
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {fixed_files}")
    print(f"Files with errors: {len(error_files)}")
    
    if error_files:
        print(f"\nFiles with errors:")
        for error_file in error_files:
            print(f"  - {error_file}")
    
    print(f"\nAll fixes completed!")
    print(f"Backup files created with .backup extension")

if __name__ == "__main__":
    main()