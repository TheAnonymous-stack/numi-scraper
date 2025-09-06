import json
import os
import glob
from typing import Dict, List, Set

def get_json_files_info() -> Dict[str, List[str]]:
    """Get information about all JSON files and their question numbers"""
    json_files = glob.glob("Gr6_*_variations.json")
    json_info = {}
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            question_numbers = []
            for item in data:
                if 'question_number' in item:
                    question_numbers.append(item['question_number'])
            
            json_info[json_file] = question_numbers
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    return json_info

def get_html_files_info() -> Dict[str, List[str]]:
    """Get information about all HTML files grouped by their base name"""
    html_files = glob.glob("HTML/*.html")
    html_info = {}
    
    for html_file in html_files:
        basename = os.path.basename(html_file)
        
        # Extract base pattern (e.g., "Gr6_15_E5" from "Gr6_15_E5_1_1.html")
        parts = basename.replace('.html', '').split('_')
        if len(parts) >= 3:
            base = f"{parts[0]}_{parts[1]}_{parts[2]}"  # Gr6_15_E5
            
            if base not in html_info:
                html_info[base] = []
            html_info[base].append(basename)
    
    return html_info

def check_json_html_consistency():
    """Check consistency between JSON and HTML files"""
    json_info = get_json_files_info()
    html_info = get_html_files_info()
    
    print("JSON-HTML Linking Verification")
    print("=" * 50)
    
    issues = []
    
    # Check each JSON file
    for json_file, question_numbers in json_info.items():
        # Extract base name from JSON file (e.g., "Gr6_15_E5" from "Gr6_15_E5_variations.json")
        base_name = json_file.replace('_variations.json', '')
        
        print(f"\nChecking: {json_file}")
        print(f"  Base name: {base_name}")
        print(f"  Questions: {len(question_numbers)}")
        
        if base_name in html_info:
            html_files = html_info[base_name]
            print(f"  HTML files: {len(html_files)} found")
            
            # Check if we have HTML files for each question
            expected_html_count = len(question_numbers) * 51  # 51 variations per question
            actual_html_count = len(html_files)
            
            if actual_html_count != expected_html_count:
                issue = f"{json_file}: Expected ~{expected_html_count} HTML files, found {actual_html_count}"
                issues.append(issue)
                print(f"  WARNING: {issue}")
            else:
                print(f"  OK: HTML file count matches expected")
        else:
            issue = f"{json_file}: No matching HTML files found for base '{base_name}'"
            issues.append(issue)
            print(f"  ERROR: {issue}")
    
    # Check for orphaned HTML files
    json_bases = {json_file.replace('_variations.json', '') for json_file in json_info.keys()}
    html_bases = set(html_info.keys())
    
    orphaned_html = html_bases - json_bases
    if orphaned_html:
        print(f"\nOrphaned HTML file groups (no matching JSON):")
        for orphan in sorted(orphaned_html):
            print(f"  - {orphan} ({len(html_info[orphan])} files)")
            issues.append(f"Orphaned HTML group: {orphan}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print(f"SUMMARY")
    print(f"=" * 50)
    print(f"JSON files processed: {len(json_info)}")
    print(f"HTML file groups: {len(html_info)}")
    print(f"Issues found: {len(issues)}")
    
    if issues:
        print(f"\nISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print(f"\nAll JSON-HTML linking appears correct!")
    
    return len(issues) == 0

def validate_json_structure():
    """Validate all JSON files have correct structure"""
    json_files = glob.glob("Gr6_*_variations.json")
    issues = []
    
    print(f"\nJSON Structure Validation")
    print("=" * 30)
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_issues = []
            
            # Check it's a list
            if not isinstance(data, list):
                file_issues.append("Root should be a list")
            
            # Check each item
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    file_issues.append(f"Item {i}: Should be an object")
                    continue
                
                # Check required fields
                required_fields = ['skills', 'question_text', 'tag', 'question_number']
                for field in required_fields:
                    if field not in item:
                        file_issues.append(f"Item {i}: Missing field '{field}'")
                
                # Check for remaining problematic patterns
                item_str = json.dumps(item)
                if '\\_\\_' in item_str:
                    file_issues.append(f"Item {i}: Still contains \\_\\_ patterns")
            
            if file_issues:
                issues.extend([f"{json_file}: {issue}" for issue in file_issues])
                print(f"  {json_file}: {len(file_issues)} issues")
            else:
                print(f"  {json_file}: OK")
                
        except Exception as e:
            issues.append(f"{json_file}: Error reading file - {e}")
            print(f"  {json_file}: ERROR - {e}")
    
    print(f"\nStructure validation: {len(issues)} issues found")
    return len(issues) == 0

if __name__ == "__main__":
    print("Grade 6 JSON/HTML Verification Script")
    print("=" * 60)
    
    # Run all validations
    linking_ok = check_json_html_consistency()
    structure_ok = validate_json_structure()
    
    print(f"\n" + "=" * 60)
    print(f"FINAL RESULTS")
    print(f"=" * 60)
    print(f"JSON-HTML linking: {'PASS' if linking_ok else 'FAIL'}")
    print(f"JSON structure: {'PASS' if structure_ok else 'FAIL'}")
    print(f"Overall status: {'PASS - All good!' if linking_ok and structure_ok else 'FAIL - Issues found'}")