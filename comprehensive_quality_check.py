import json
import os
import glob
from collections import defaultdict

def check_variation_file(filepath):
    """Check a single variation file for quality issues"""
    issues = []
    filename = os.path.basename(filepath)
    
    # Extract expected pattern from filename
    try:
        parts = filename.replace('_variations.json', '').split('_')
        grade = parts[0]  # Gr6
        week = parts[1]   # week number
        exercise = parts[2]  # E1, E2, etc
        base_tag = f"{grade}_{week}_{exercise}"
    except:
        issues.append(f"Invalid filename format: {filename}")
        return issues, None
    
    # Try to read and parse JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        issues.append(f"JSON parsing error: {e}")
        return issues, None
    except Exception as e:
        issues.append(f"File read error: {e}")
        return issues, None
    
    # Check if data is a list
    if not isinstance(data, list):
        issues.append("Data is not a list")
        return issues, None
    
    # Check number of variations
    num_variations = len(data)
    if num_variations != 51:
        issues.append(f"Expected 51 variations, found {num_variations}")
    
    # Track tags for duplicates
    tags_seen = set()
    
    # Check each variation
    for i, variation in enumerate(data, 1):
        if not isinstance(variation, dict):
            issues.append(f"Variation {i} is not a dictionary")
            continue
        
        # Check required fields
        required_fields = ['tag', 'question', 'solution', 'difficulty', 'hint']
        for field in required_fields:
            if field not in variation:
                issues.append(f"Variation {i} missing required field: {field}")
        
        # Check tag format
        if 'tag' in variation:
            tag = variation['tag']
            expected_tag = f"{base_tag}_V{i}"
            
            if tag != expected_tag:
                issues.append(f"Variation {i} has incorrect tag: expected '{expected_tag}', got '{tag}'")
            
            # Check for duplicate tags
            if tag in tags_seen:
                issues.append(f"Duplicate tag found: {tag}")
            tags_seen.add(tag)
        
        # Check for empty or None values in critical fields
        if 'question' in variation:
            if not variation['question'] or variation['question'].strip() == '':
                issues.append(f"Variation {i} has empty question")
        
        if 'solution' in variation:
            if variation['solution'] is None or str(variation['solution']).strip() == '':
                issues.append(f"Variation {i} has empty solution")
        
        # Check difficulty is valid
        if 'difficulty' in variation:
            valid_difficulties = ['easy', 'medium', 'hard']
            if variation['difficulty'] not in valid_difficulties:
                issues.append(f"Variation {i} has invalid difficulty: {variation['difficulty']}")
    
    # Check if V1 (template) exists
    if num_variations > 0:
        first_variation = data[0]
        if 'tag' in first_variation:
            if not first_variation['tag'].endswith('_V1'):
                issues.append("First variation is not marked as V1 (template)")
    
    return issues, num_variations

def main():
    # Find all Gr6 variation files
    pattern = "Gr6_*_E*_variations.json"
    files = glob.glob(pattern)
    files.sort()
    
    print(f"Found {len(files)} Grade 6 variation files to check\n")
    print("=" * 80)
    
    # Statistics
    total_files = len(files)
    files_with_issues = []
    files_passing = []
    all_issues = defaultdict(list)
    
    # Check each file
    for filepath in files:
        filename = os.path.basename(filepath)
        issues, num_variations = check_variation_file(filepath)
        
        if issues:
            files_with_issues.append(filename)
            all_issues[filename] = issues
        else:
            files_passing.append(filename)
    
    # Print detailed report
    print("\nDETAILED QUALITY CHECK REPORT")
    print("=" * 80)
    
    print(f"\nTotal files checked: {total_files}")
    print(f"Files passing all checks: {len(files_passing)}")
    print(f"Files with issues: {len(files_with_issues)}")
    
    if files_with_issues:
        print("\n" + "=" * 80)
        print("FILES WITH ISSUES:")
        print("=" * 80)
        
        for filename in sorted(files_with_issues):
            print(f"\n{filename}:")
            for issue in all_issues[filename]:
                print(f"  - {issue}")
    
    print("\n" + "=" * 80)
    print("FILES PASSING ALL CHECKS:")
    print("=" * 80)
    
    if files_passing:
        # Print in columns for readability
        for i in range(0, len(files_passing), 3):
            row = files_passing[i:i+3]
            print("  " + " | ".join(f"{f:30}" for f in row))
    else:
        print("  None")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS:")
    print("=" * 80)
    
    if total_files > 0:
        pass_rate = (len(files_passing) / total_files) * 100
        print(f"Pass rate: {pass_rate:.1f}%")
        
        if files_with_issues:
            # Count types of issues
            issue_types = defaultdict(int)
            for filename, issues in all_issues.items():
                for issue in issues:
                    if "Expected 51 variations" in issue:
                        issue_types["Wrong number of variations"] += 1
                    elif "missing required field" in issue:
                        issue_types["Missing required fields"] += 1
                    elif "incorrect tag" in issue:
                        issue_types["Incorrect tag format"] += 1
                    elif "Duplicate tag" in issue:
                        issue_types["Duplicate tags"] += 1
                    elif "empty" in issue.lower():
                        issue_types["Empty fields"] += 1
                    elif "JSON parsing error" in issue:
                        issue_types["JSON parsing errors"] += 1
                    else:
                        issue_types["Other issues"] += 1
            
            print("\nIssue breakdown:")
            for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {issue_type}: {count}")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    if not files_with_issues:
        print("✓ All files pass quality checks! No immediate action required.")
    else:
        print("Issues found that require attention:")
        
        # Check for critical issues
        critical_files = []
        for filename, issues in all_issues.items():
            for issue in issues:
                if "JSON parsing error" in issue or "Expected 51 variations" in issue:
                    critical_files.append(filename)
                    break
        
        if critical_files:
            print(f"\n1. CRITICAL: {len(set(critical_files))} files have structural issues:")
            for f in sorted(set(critical_files))[:5]:  # Show first 5
                print(f"   - {f}")
            if len(set(critical_files)) > 5:
                print(f"   ... and {len(set(critical_files)) - 5} more")
            print("   These files need immediate repair or regeneration.")
        
        # Check for tag issues
        tag_issue_files = []
        for filename, issues in all_issues.items():
            for issue in issues:
                if "tag" in issue.lower():
                    tag_issue_files.append(filename)
                    break
        
        if tag_issue_files:
            print(f"\n2. Tag Issues: {len(set(tag_issue_files))} files have tag-related problems")
            print("   Tags should follow format: Gr6_<week>_<exercise>_V<number>")
        
        # Check for missing fields
        missing_field_files = []
        for filename, issues in all_issues.items():
            for issue in issues:
                if "missing required field" in issue:
                    missing_field_files.append(filename)
                    break
        
        if missing_field_files:
            print(f"\n3. Missing Fields: {len(set(missing_field_files))} files have missing required fields")
            print("   All variations must have: tag, question, solution, difficulty, hint")
    
    print("\n" + "=" * 80)
    print("QUALITY CHECK COMPLETE")
    print("=" * 80)
    
    return total_files, len(files_passing), len(files_with_issues)

if __name__ == "__main__":
    main()