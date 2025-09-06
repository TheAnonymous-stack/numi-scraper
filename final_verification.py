#!/usr/bin/env python3
"""
Final verification script to validate all Grade 6 variation files.
"""
import json
import glob
import os
from collections import defaultdict

def validate_variation_file(file_path):
    """Validate a single variation file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            errors.append("File should contain a list of variations")
            return errors, warnings, 0
        
        count = len(data)
        if count != 51:
            errors.append(f"Expected 51 variations, found {count}")
        
        # Check each variation
        tags_seen = set()
        question_numbers_seen = set()
        
        for i, variation in enumerate(data):
            if not isinstance(variation, dict):
                errors.append(f"Variation {i+1} is not a dictionary")
                continue
            
            # Required fields
            required_fields = ['skills', 'tag', 'question_type', 'question_number']
            for field in required_fields:
                if field not in variation:
                    errors.append(f"Variation {i+1} missing required field: {field}")
            
            # Check tag consistency
            if 'tag' in variation:
                tags_seen.add(variation['tag'])
            
            # Check question number format
            if 'question_number' in variation:
                qnum = variation['question_number']
                question_numbers_seen.add(qnum)
                if not isinstance(qnum, str) or '_' not in qnum:
                    warnings.append(f"Variation {i+1} has unusual question_number format: {qnum}")
            
            # Check question type specific requirements
            if 'question_type' in variation:
                qtype = variation['question_type']
                
                if 'Multiple Choice' in qtype:
                    if 'correct_answers' not in variation:
                        errors.append(f"Variation {i+1} missing correct_answers for multiple choice")
                    elif isinstance(variation.get('correct_answers'), list):
                        # Check if answers are stored as letters (A, B, C) not literal text
                        answers = variation['correct_answers']
                        for ans in answers:
                            if isinstance(ans, str) and len(ans) == 1 and ans in 'ABCDEFGH':
                                continue  # Good - letter format
                            elif isinstance(ans, str) and len(ans) > 1:
                                warnings.append(f"Variation {i+1} may have literal text instead of letter for MC answer")
                                break
                
                elif 'Fill in the blank' in qtype:
                    if 'correct_answers' not in variation:
                        errors.append(f"Variation {i+1} missing correct_answers for fill in blank")
                    
                    # Check for multiple blanks vs multiple answers
                    if 'question_text' in variation:
                        blank_count = variation['question_text'].count('_')
                        if blank_count > 1 and 'correct_answers' in variation:
                            if len(variation['correct_answers']) != blank_count:
                                errors.append(f"Variation {i+1} has {blank_count} blanks but {len(variation['correct_answers'])} answers")
                            if 'orderMatter' not in variation:
                                warnings.append(f"Variation {i+1} has multiple blanks but no orderMatter field")
        
        # Check tag consistency within file
        if len(tags_seen) > 1:
            errors.append(f"Multiple tags found in file: {tags_seen}")
        
        # Check for duplicate question numbers
        if len(question_numbers_seen) != len(data):
            errors.append(f"Duplicate question numbers found")
        
    except json.JSONDecodeError as e:
        errors.append(f"JSON parsing error: {e}")
        count = 0
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        count = 0
    
    return errors, warnings, count

def main():
    """Main validation function."""
    pattern = "Gr6_*_E*_variations.json"
    files = glob.glob(pattern)
    files.sort()
    
    print("Final Grade 6 Variation Files Verification")
    print("=" * 60)
    
    total_files = 0
    valid_files = 0
    total_variations = 0
    files_with_errors = []
    files_with_warnings = []
    
    for file_path in files:
        total_files += 1
        filename = os.path.basename(file_path)
        
        errors, warnings, count = validate_variation_file(file_path)
        total_variations += count
        
        if errors:
            files_with_errors.append((filename, errors))
            status = f"ERROR ({len(errors)} issues)"
        elif warnings:
            files_with_warnings.append((filename, warnings))
            status = f"WARNING ({len(warnings)} issues)"
            valid_files += 1
        else:
            status = "VALID"
            valid_files += 1
        
        print(f"{filename:<35} Count: {count:>3} {status}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print(f"Total files checked: {total_files}")
    print(f"Valid files: {valid_files}")
    print(f"Files with errors: {len(files_with_errors)}")
    print(f"Files with warnings: {len(files_with_warnings)}")
    print(f"Total variations: {total_variations}")
    print(f"Average variations per file: {total_variations/total_files if total_files > 0 else 0:.1f}")
    
    if files_with_errors:
        print(f"\nFILES WITH ERRORS:")
        for filename, errors in files_with_errors[:10]:  # Show first 10
            print(f"  {filename}:")
            for error in errors[:3]:  # Show first 3 errors
                print(f"    - {error}")
            if len(errors) > 3:
                print(f"    ... and {len(errors)-3} more errors")
    
    if files_with_warnings:
        print(f"\nFILES WITH WARNINGS (first 5):")
        for filename, warnings in files_with_warnings[:5]:
            print(f"  {filename}:")
            for warning in warnings[:2]:  # Show first 2 warnings
                print(f"    - {warning}")
            if len(warnings) > 2:
                print(f"    ... and {len(warnings)-2} more warnings")
    
    print(f"\nCONCLUSION:")
    if len(files_with_errors) == 0:
        print("SUCCESS: All Grade 6 variation files have exactly 51 variations each!")
        print("SUCCESS: No critical errors found in the variation files.")
        if len(files_with_warnings) == 0:
            print("SUCCESS: All files are fully compliant with requirements.")
        else:
            print(f"WARNING: {len(files_with_warnings)} files have minor warnings that should be reviewed.")
    else:
        print(f"ERROR: {len(files_with_errors)} files have errors that need to be fixed.")

if __name__ == "__main__":
    main()