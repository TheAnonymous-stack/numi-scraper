#!/usr/bin/env python3
"""
Fix HTML Step Label Issues - Comprehensive Script

This script fixes step labels in HTML files that incorrectly include exercise identifiers.

WRONG: label="Gr6_XX_EY_T_V_step_N"  (has exercise identifier EY)
CORRECT: label="Gr6_XX_T_V_step_N"    (no exercise identifier)

Where:
- XX = week number
- EY = exercise identifier (E1, E2, E3, etc) - should NOT be in step labels
- T = tag number
- V = variation number
- N = step number
"""

import os
import re
import glob

# List of exercises to fix
EXERCISES_TO_FIX = [
    'Gr6_54_E3', 'Gr6_55_E1', 'Gr6_1_E4', 'Gr6_1_E5', 'Gr6_2_E1', 'Gr6_3_E4',
    'Gr6_5_E1', 'Gr6_3_E2', 'Gr6_15_E5', 'Gr6_16_E1', 'Gr6_23_E1', 'Gr6_23_E2',
    'Gr6_23_E3', 'Gr6_24_E1', 'Gr6_24_E2', 'Gr6_24_E3', 'Gr6_28_E3', 'Gr6_33_E1',
    'Gr6_33_E2', 'Gr6_34_E3', 'Gr6_35_E1', 'Gr6_36_E1', 'Gr6_42_E4', 'Gr6_43_E2',
    'Gr6_44_E1', 'Gr6_44_E2', 'Gr6_44_E3', 'Gr6_45_E2', 'Gr6_45_E4', 'Gr6_50_E1',
    'Gr6_50_E2', 'Gr6_51_E1', 'Gr6_51_E2', 'Gr6_51_E3', 'Gr6_51_E4', 'Gr6_52_E1',
    'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_48_E1'
]

def fix_step_labels_in_file(file_path):
    """
    Fix step labels in a single HTML file.

    Returns:
        tuple: (changes_made, list_of_changes)
    """
    changes_made = 0
    changes_list = []

    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Extract exercise info from filename
        filename = os.path.basename(file_path)
        # Pattern: Gr6_XX_EY_T_V.html
        filename_match = re.match(r'Gr6_(\d+)_E(\d+)_(\d+)_(\d+)\.html', filename)

        if not filename_match:
            print(f"Warning: Could not parse filename {filename}")
            return 0, []

        week_num = filename_match.group(1)
        exercise_num = filename_match.group(2)
        tag_num = filename_match.group(3)
        variation_num = filename_match.group(4)

        # Pattern to find step labels that need fixing
        # Match: label="Gr6_XX_EY_T_V_step_N"
        step_pattern = rf'label="(Gr6_{week_num}_E{exercise_num}_{tag_num}_{variation_num}_step_\d+)"'

        def replace_step_label(match):
            nonlocal changes_made, changes_list
            old_label = match.group(1)
            # Remove the _EY part: Gr6_XX_EY_T_V_step_N -> Gr6_XX_T_V_step_N
            new_label = re.sub(rf'_E{exercise_num}_', '_', old_label)

            changes_made += 1
            changes_list.append(f"  {old_label} -> {new_label}")

            return f'label="{new_label}"'

        # Apply the fix
        content = re.sub(step_pattern, replace_step_label, content)

        # Only write if changes were made
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, []

    return changes_made, changes_list

def main():
    """Main function to process all HTML files for specified exercises."""
    print("HTML Step Label Fixer - Comprehensive")
    print("=" * 50)
    print(f"Processing {len(EXERCISES_TO_FIX)} exercises")
    print()

    total_files_changed = 0
    total_changes_made = 0
    detailed_report = []

    # Process each exercise
    for exercise in EXERCISES_TO_FIX:
        print(f"Processing {exercise}...")

        # Find all HTML files for this exercise
        html_pattern = f"html/{exercise}_*.html"
        html_files = glob.glob(html_pattern)

        if not html_files:
            print(f"  No HTML files found for {exercise}")
            continue

        exercise_files_changed = 0
        exercise_changes_made = 0
        exercise_details = []

        # Process each HTML file
        for html_file in sorted(html_files):
            changes_count, changes_list = fix_step_labels_in_file(html_file)

            if changes_count > 0:
                exercise_files_changed += 1
                exercise_changes_made += changes_count

                file_detail = {
                    'file': html_file,
                    'changes_count': changes_count,
                    'changes_list': changes_list
                }
                exercise_details.append(file_detail)

        # Report for this exercise
        if exercise_files_changed > 0:
            print(f"  FIXED: {exercise_files_changed} files changed, {exercise_changes_made} total changes")
            total_files_changed += exercise_files_changed
            total_changes_made += exercise_changes_made

            detailed_report.append({
                'exercise': exercise,
                'files_changed': exercise_files_changed,
                'changes_made': exercise_changes_made,
                'details': exercise_details
            })
        else:
            print(f"  No changes needed for {exercise}")

    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total exercises processed: {len(EXERCISES_TO_FIX)}")
    print(f"Total files changed: {total_files_changed}")
    print(f"Total label changes made: {total_changes_made}")

    # Detailed report
    if detailed_report:
        print()
        print("DETAILED CHANGES:")
        print("-" * 30)

        for report in detailed_report[:5]:  # Show first 5 exercises in detail
            exercise = report['exercise']
            print(f"\n{exercise}:")

            for file_detail in report['details'][:3]:  # Show first 3 files per exercise
                filename = os.path.basename(file_detail['file'])
                print(f"  {filename} ({file_detail['changes_count']} changes):")
                for change in file_detail['changes_list']:
                    print(f"    {change}")

        if len(detailed_report) > 5:
            print(f"\n... and {len(detailed_report) - 5} more exercises with changes")

    print("\nAll specified exercises have been processed!")
    return total_files_changed, total_changes_made

if __name__ == "__main__":
    files_changed, changes_made = main()