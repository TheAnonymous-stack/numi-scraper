import json
import glob
import re
import os
from collections import defaultdict

def check_all_grade6_files():
    """Comprehensive check of ALL Grade 6 variation files"""
    
    # Get all Grade 6 variation files
    all_files = sorted(glob.glob('Gr6_*_variations.json'))
    
    print(f"Checking {len(all_files)} Grade 6 variation files...")
    print("=" * 60)
    
    # Track issues
    issues = defaultdict(list)
    correct_files = []
    
    # Check each file
    for file_path in all_files:
        filename = os.path.basename(file_path)
        
        # Extract week and exercise number from filename
        match = re.search(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
        if not match:
            issues['invalid_filename'].append(filename)
            continue
        
        week_num = match.group(1)
        exercise_num = match.group(2)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get variations (handle both list and dict format)
            if isinstance(data, list):
                variations = data
            else:
                variations = data.get('variations', [])
            
            # Check 1: Exactly 51 variations
            if len(variations) != 51:
                issues['wrong_count'].append(f"{filename}: {len(variations)} variations (should be 51)")
            
            # Check 2: Question number format
            format_issues = []
            for i, variation in enumerate(variations, 1):
                expected_qn = f"{exercise_num}_{i}"
                actual_qn = variation.get('question_number', '')
                
                if actual_qn != expected_qn:
                    format_issues.append(f"Variation {i}: has '{actual_qn}' should be '{expected_qn}'")
            
            if format_issues:
                issues['wrong_format'].append(f"{filename}: {len(format_issues)} format issues")
                if len(format_issues) <= 3:  # Show details for files with few issues
                    for issue in format_issues:
                        issues['format_details'].append(f"  {filename} - {issue}")
            
            # Check 3: Other important fields
            for i, variation in enumerate(variations, 1):
                # Check question_type
                q_type = variation.get('question_type', '')
                if q_type not in ['Fill in the blank', 'Multiple fill in the blank', 'Multiple Choice']:
                    issues['invalid_type'].append(f"{filename} variation {i}: invalid type '{q_type}'")
                
                # Check correct_answers exists
                if 'correct_answers' not in variation:
                    issues['missing_answers'].append(f"{filename} variation {i}: missing correct_answers")
                
                # Check question_text exists
                if 'question_text' not in variation:
                    issues['missing_text'].append(f"{filename} variation {i}: missing question_text")
            
            # If no issues, mark as correct
            if filename not in [item.split(':')[0] for sublist in issues.values() for item in sublist]:
                correct_files.append(filename)
                
        except Exception as e:
            issues['file_errors'].append(f"{filename}: {str(e)}")
    
    # Print results
    print("\nRESULTS:")
    print("=" * 60)
    
    if not any(issues.values()):
        print(f"✓ ALL {len(all_files)} files are correctly formatted!")
        print(f"✓ All files have exactly 51 variations")
        print(f"✓ All question_number fields follow the correct format")
    else:
        print(f"Files checked: {len(all_files)}")
        print(f"Correct files: {len(correct_files)}")
        print(f"Files with issues: {len(all_files) - len(correct_files)}")
        print()
        
        if issues['wrong_count']:
            print(f"\n❌ Files with wrong variation count ({len(issues['wrong_count'])}):")
            for issue in issues['wrong_count'][:5]:
                print(f"  - {issue}")
            if len(issues['wrong_count']) > 5:
                print(f"  ... and {len(issues['wrong_count']) - 5} more")
        
        if issues['wrong_format']:
            print(f"\n❌ Files with wrong question_number format ({len(issues['wrong_format'])}):")
            for issue in issues['wrong_format'][:5]:
                print(f"  - {issue}")
            if len(issues['wrong_format']) > 5:
                print(f"  ... and {len(issues['wrong_format']) - 5} more")
        
        if issues['format_details'] and len(issues['format_details']) <= 10:
            print("\nFormat issue details:")
            for detail in issues['format_details']:
                print(detail)
        
        if issues['invalid_type']:
            print(f"\n❌ Invalid question types ({len(issues['invalid_type'])}):")
            for issue in issues['invalid_type'][:3]:
                print(f"  - {issue}")
        
        if issues['missing_answers']:
            print(f"\n❌ Missing correct_answers ({len(issues['missing_answers'])}):")
            for issue in issues['missing_answers'][:3]:
                print(f"  - {issue}")
        
        if issues['file_errors']:
            print(f"\n❌ File errors ({len(issues['file_errors'])}):")
            for error in issues['file_errors'][:3]:
                print(f"  - {error}")
    
    # Summary by week
    print("\n" + "=" * 60)
    print("WEEK-BY-WEEK SUMMARY:")
    print("=" * 60)
    
    week_files = defaultdict(list)
    for f in all_files:
        match = re.search(r'Gr6_(\d+)_E\d+_variations\.json', os.path.basename(f))
        if match:
            week_files[int(match.group(1))].append(os.path.basename(f))
    
    print(f"Weeks covered: {sorted(week_files.keys())}")
    print(f"Total weeks: {len(week_files)}")
    
    # Check for missing weeks
    all_weeks = set(range(1, 56))
    present_weeks = set(week_files.keys())
    missing_weeks = all_weeks - present_weeks
    
    if missing_weeks:
        print(f"\n⚠ Missing weeks: {sorted(missing_weeks)}")
    else:
        print(f"\n✓ All weeks from 1 to 55 have variation files")
    
    # Files per week
    files_per_week = {week: len(files) for week, files in week_files.items()}
    min_files = min(files_per_week.values())
    max_files = max(files_per_week.values())
    
    print(f"\nFiles per week: {min_files} to {max_files}")
    
    # Show weeks with unusual file counts
    unusual_weeks = {week: count for week, count in files_per_week.items() 
                     if count < 3 or count > 4}
    if unusual_weeks:
        print(f"\nWeeks with unusual file counts:")
        for week, count in sorted(unusual_weeks.items()):
            print(f"  Week {week}: {count} files")
    
    return issues, correct_files

if __name__ == "__main__":
    issues, correct_files = check_all_grade6_files()
    
    # Return exit code based on results
    if not any(issues.values()):
        exit(0)
    else:
        exit(1)