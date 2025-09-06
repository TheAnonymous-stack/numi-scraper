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
        issues.append("Invalid filename format")
        return issues, None, {}
    
    # Try to read and parse JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        issues.append("JSON parsing error")
        return issues, None, {}
    except Exception as e:
        issues.append("File read error")
        return issues, None, {}
    
    # Check if data is a list
    if not isinstance(data, list):
        issues.append("Data is not a list")
        return issues, None, {}
    
    # Statistics for this file
    stats = {
        'num_variations': len(data),
        'missing_fields_count': 0,
        'tag_issues_count': 0,
        'duplicate_tags_count': 0,
        'empty_fields_count': 0
    }
    
    # Check number of variations
    if stats['num_variations'] != 51:
        issues.append(f"Wrong number of variations: {stats['num_variations']}")
    
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
                stats['missing_fields_count'] += 1
        
        # Check tag format
        if 'tag' in variation:
            tag = variation['tag']
            expected_tag = f"{base_tag}_V{i}"
            
            if tag != expected_tag:
                stats['tag_issues_count'] += 1
            
            # Check for duplicate tags
            if tag in tags_seen:
                stats['duplicate_tags_count'] += 1
            tags_seen.add(tag)
        
        # Check for empty values
        if 'question' in variation:
            if not variation['question'] or variation['question'].strip() == '':
                stats['empty_fields_count'] += 1
        
        if 'solution' in variation:
            if variation['solution'] is None or str(variation['solution']).strip() == '':
                stats['empty_fields_count'] += 1
    
    # Create summary of issues
    if stats['missing_fields_count'] > 0:
        issues.append(f"Missing required fields: {stats['missing_fields_count']} instances")
    if stats['tag_issues_count'] > 0:
        issues.append(f"Tag format issues: {stats['tag_issues_count']} instances")
    if stats['duplicate_tags_count'] > 0:
        issues.append(f"Duplicate tags: {stats['duplicate_tags_count']} instances")
    if stats['empty_fields_count'] > 0:
        issues.append(f"Empty fields: {stats['empty_fields_count']} instances")
    
    return issues, stats['num_variations'], stats

def main():
    # Find all Gr6 variation files
    pattern = "Gr6_*_E*_variations.json"
    files = glob.glob(pattern)
    files.sort()
    
    print("=" * 80)
    print("COMPREHENSIVE QUALITY CHECK REPORT FOR GRADE 6 VARIATION FILES")
    print("=" * 80)
    print(f"\nTotal files found: {len(files)}")
    
    # Categories
    files_passing = []
    files_with_issues = {}
    
    # Issue type counters
    issue_types = defaultdict(int)
    
    # Check each file
    for filepath in files:
        filename = os.path.basename(filepath)
        issues, num_variations, stats = check_variation_file(filepath)
        
        if issues:
            files_with_issues[filename] = issues
            # Categorize issues
            for issue in issues:
                if "JSON parsing error" in issue:
                    issue_types["JSON Parsing Errors"] += 1
                elif "Wrong number of variations" in issue:
                    issue_types["Wrong Variation Count"] += 1
                elif "Missing required fields" in issue:
                    issue_types["Missing Required Fields"] += 1
                elif "Tag format issues" in issue:
                    issue_types["Tag Format Issues"] += 1
                elif "Duplicate tags" in issue:
                    issue_types["Duplicate Tags"] += 1
                elif "Empty fields" in issue:
                    issue_types["Empty Fields"] += 1
                else:
                    issue_types["Other Issues"] += 1
        else:
            files_passing.append(filename)
    
    # Print Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\n[PASS] Files passing ALL checks: {len(files_passing)}")
    print(f"[FAIL] Files with issues: {len(files_with_issues)}")
    
    if len(files) > 0:
        pass_rate = (len(files_passing) / len(files)) * 100
        print(f"\nOverall pass rate: {pass_rate:.1f}%")
    
    # Issue breakdown
    if issue_types:
        print("\n" + "-" * 40)
        print("ISSUE BREAKDOWN:")
        print("-" * 40)
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue_type}: {count} files")
    
    # List files with critical issues
    print("\n" + "=" * 80)
    print("CRITICAL ISSUES (Files requiring immediate attention):")
    print("=" * 80)
    
    critical_files = []
    for filename, issues in files_with_issues.items():
        for issue in issues:
            if "JSON parsing error" in issue or "Wrong number of variations" in issue:
                critical_files.append(filename)
                break
    
    if critical_files:
        print(f"\n{len(critical_files)} files with critical structural issues:")
        for f in sorted(critical_files)[:20]:  # Show first 20
            print(f"  - {f}")
        if len(critical_files) > 20:
            print(f"  ... and {len(critical_files) - 20} more")
    else:
        print("\n[OK] No critical structural issues found")
    
    # Files with tag/field issues
    print("\n" + "=" * 80)
    print("FILES WITH DATA QUALITY ISSUES:")
    print("=" * 80)
    
    data_quality_files = []
    for filename, issues in files_with_issues.items():
        for issue in issues:
            if any(x in issue for x in ["Missing required fields", "Tag format", "Duplicate tags", "Empty fields"]):
                data_quality_files.append(filename)
                break
    
    if data_quality_files:
        print(f"\n{len(data_quality_files)} files with data quality issues:")
        # Group by week for better readability
        by_week = defaultdict(list)
        for f in data_quality_files:
            week = f.split('_')[1]
            by_week[week].append(f)
        
        for week in sorted(by_week.keys(), key=int):
            print(f"\n  Week {week}:")
            for f in sorted(by_week[week]):
                print(f"    - {f}")
    
    # Files passing all checks
    if files_passing:
        print("\n" + "=" * 80)
        print(f"FILES PASSING ALL CHECKS ({len(files_passing)} files):")
        print("=" * 80)
        
        # Group by week
        by_week = defaultdict(list)
        for f in files_passing:
            week = f.split('_')[1]
            by_week[week].append(f)
        
        if by_week:
            for week in sorted(by_week.keys(), key=int):
                print(f"\n  Week {week}: {', '.join(sorted(by_week[week]))}")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    if not files_with_issues:
        print("\n[SUCCESS] All files pass quality checks! No action required.")
    else:
        print("\n1. IMMEDIATE ACTIONS REQUIRED:")
        
        if critical_files:
            print(f"\n   - Fix {len(critical_files)} files with structural issues")
            print("     These files have incorrect JSON structure or wrong variation counts")
        
        if data_quality_files:
            print(f"\n   - Review {len(data_quality_files)} files with data quality issues")
            print("     These files need tag corrections and field completeness checks")
        
        print("\n2. QUALITY IMPROVEMENT STEPS:")
        print("\n   - Ensure all files have exactly 51 variations")
        print("   - Verify tags follow format: Gr6_<week>_<exercise>_V<1-51>")
        print("   - Check all required fields are present: tag, question, solution, difficulty, hint")
        print("   - Eliminate duplicate tags within files")
        print("   - Ensure no empty question or solution fields")
        
        print("\n3. PRIORITY ORDER:")
        if issue_types:
            priority = []
            if issue_types.get("JSON Parsing Errors", 0) > 0:
                priority.append("Fix JSON parsing errors first")
            if issue_types.get("Wrong Variation Count", 0) > 0:
                priority.append("Correct files with wrong number of variations")
            if issue_types.get("Tag Format Issues", 0) > 0:
                priority.append("Fix tag formatting issues")
            if issue_types.get("Missing Required Fields", 0) > 0:
                priority.append("Add missing required fields")
            
            for i, p in enumerate(priority, 1):
                print(f"   {i}. {p}")
    
    print("\n" + "=" * 80)
    print("END OF REPORT")
    print("=" * 80)

if __name__ == "__main__":
    main()