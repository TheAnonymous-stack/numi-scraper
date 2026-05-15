#!/usr/bin/env python3
"""
Verification Script for HTML Step Label Fixes

This script verifies that step labels have been correctly fixed by:
1. Checking that no step labels contain exercise identifiers (EY)
2. Confirming all step labels follow the pattern Gr6_XX_T_V_step_N
3. Providing a summary of the fixes
"""

import os
import re
import glob

# List of exercises that were processed
PROCESSED_EXERCISES = [
    'Gr6_54_E3', 'Gr6_55_E1', 'Gr6_1_E4', 'Gr6_1_E5', 'Gr6_2_E1', 'Gr6_3_E4',
    'Gr6_5_E1', 'Gr6_3_E2', 'Gr6_15_E5', 'Gr6_16_E1', 'Gr6_23_E1', 'Gr6_23_E2',
    'Gr6_23_E3', 'Gr6_24_E1', 'Gr6_24_E2', 'Gr6_24_E3', 'Gr6_28_E3', 'Gr6_33_E1',
    'Gr6_33_E2', 'Gr6_34_E3', 'Gr6_35_E1', 'Gr6_36_E1', 'Gr6_42_E4', 'Gr6_43_E2',
    'Gr6_44_E1', 'Gr6_44_E2', 'Gr6_44_E3', 'Gr6_45_E2', 'Gr6_45_E4', 'Gr6_50_E1',
    'Gr6_50_E2', 'Gr6_51_E1', 'Gr6_51_E2', 'Gr6_51_E3', 'Gr6_51_E4', 'Gr6_52_E1',
    'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_48_E1'
]

def verify_file(file_path):
    """
    Verify a single HTML file for correct step label format.

    Returns:
        tuple: (issues_found, list_of_issues)
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = os.path.basename(file_path)

        # Find all label attributes
        label_pattern = r'label="([^"]+)"'
        labels = re.findall(label_pattern, content)

        for label in labels:
            # Check if it's a step label
            if '_step_' in label:
                # Check if it still contains exercise identifier
                if re.search(r'Gr6_\d+_E\d+_\d+_\d+_step_\d+', label):
                    issues.append(f"INCORRECT step label found: {label}")
                # Check if it's now in correct format
                elif not re.search(r'Gr6_\d+_\d+_\d+_step_\d+', label):
                    issues.append(f"MALFORMED step label found: {label}")

    except Exception as e:
        issues.append(f"Error reading file: {e}")

    return len(issues), issues

def get_sample_changes():
    """
    Show some sample files that were changed to demonstrate the fixes.
    """
    sample_files = [
        'C:\\Users\\kapil\\numi-scraper\\html\\Gr6_24_E3_3_10.html',
        'C:\\Users\\kapil\\numi-scraper\\html\\Gr6_24_E3_3_2.html',
        'C:\\Users\\kapil\\numi-scraper\\html\\Gr6_23_E1_1_1.html'
    ]

    print("SAMPLE OF FIXED FILES:")
    print("-" * 30)

    for file_path in sample_files:
        if os.path.exists(file_path):
            print(f"\n{os.path.basename(file_path)}:")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find step labels
                step_labels = re.findall(r'label="([^"]*_step_[^"]*)"', content)
                if step_labels:
                    for label in step_labels:
                        print(f"  Step label: {label}")
                else:
                    print("  No step labels found")

            except Exception as e:
                print(f"  Error reading file: {e}")
        else:
            print(f"\n{os.path.basename(file_path)}: File not found")

def main():
    """Main verification function."""
    print("HTML Step Label Fix Verification")
    print("=" * 40)

    total_files_checked = 0
    total_issues_found = 0
    exercises_with_issues = 0

    # Check each exercise
    for exercise in PROCESSED_EXERCISES:
        print(f"\nVerifying {exercise}...")

        # Find all HTML files for this exercise
        html_pattern = f"html/{exercise}_*.html"
        html_files = glob.glob(html_pattern)

        if not html_files:
            print(f"  No HTML files found")
            continue

        exercise_issues = 0
        exercise_files = 0

        # Check each file
        for html_file in html_files:
            if re.match(r'.*Gr6_\d+_E\d+_\d+_\d+\.html$', html_file):
                exercise_files += 1
                total_files_checked += 1

                issues_count, issues_list = verify_file(html_file)

                if issues_count > 0:
                    exercise_issues += issues_count
                    total_issues_found += issues_count
                    print(f"  ISSUES in {os.path.basename(html_file)}:")
                    for issue in issues_list:
                        print(f"    - {issue}")

        if exercise_issues == 0 and exercise_files > 0:
            print(f"  VERIFIED: {exercise_files} files, all step labels correct")
        elif exercise_files > 0:
            print(f"  ISSUES: {exercise_issues} problems in {exercise_files} files")
            exercises_with_issues += 1
        else:
            print(f"  WARNING: No standard HTML files found")

    print()
    print("=" * 40)
    print("VERIFICATION SUMMARY")
    print("=" * 40)
    print(f"Total exercises processed: {len(PROCESSED_EXERCISES)}")
    print(f"Total HTML files checked: {total_files_checked}")
    print(f"Total issues found: {total_issues_found}")
    print(f"Exercises with issues: {exercises_with_issues}")

    if total_issues_found == 0:
        print("\nSUCCESS: All step labels are correctly formatted!")
        print("   Pattern: Gr6_XX_T_V_step_N (exercise identifier EY removed)")
    else:
        print(f"\nISSUES REMAINING: {total_issues_found} problems need attention")

    # Show sample changes
    print()
    get_sample_changes()

    return total_issues_found

if __name__ == "__main__":
    issues = main()