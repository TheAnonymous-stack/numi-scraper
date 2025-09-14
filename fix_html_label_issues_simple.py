#!/usr/bin/env python3
"""
Simple HTML Label Fix Script for Grade 6 Exercises

This script fixes HTML label issues where labels in HTML files have incorrect variation numbers
that don't match the filename variation numbers.
"""

import os
import re
from pathlib import Path

# Target exercises to fix
TARGET_EXERCISES = [
    'Gr6_54_E3', 'Gr6_55_E1', 'Gr6_1_E4', 'Gr6_1_E5', 'Gr6_2_E1', 'Gr6_3_E4',
    'Gr6_5_E1', 'Gr6_3_E2', 'Gr6_15_E5', 'Gr6_16_E1', 'Gr6_23_E1', 'Gr6_23_E2',
    'Gr6_23_E3', 'Gr6_24_E1', 'Gr6_24_E2', 'Gr6_24_E3', 'Gr6_28_E3', 'Gr6_33_E1',
    'Gr6_33_E2', 'Gr6_34_E3', 'Gr6_35_E1', 'Gr6_36_E1', 'Gr6_42_E4', 'Gr6_43_E2',
    'Gr6_44_E1', 'Gr6_44_E2', 'Gr6_44_E3', 'Gr6_45_E2', 'Gr6_45_E4', 'Gr6_50_E1',
    'Gr6_50_E2', 'Gr6_51_E1', 'Gr6_51_E2', 'Gr6_51_E3', 'Gr6_51_E4', 'Gr6_52_E1',
    'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_48_E1'
]

def extract_exercise_info_from_filename(filename):
    """Extract exercise info from filename like Gr6_24_E3_3_1.html"""
    pattern = r'^(Gr6)_(\d+)_(E\d+)_(\d+)_(\d+)\.html$'
    match = re.match(pattern, filename)
    if match:
        return match.groups()  # (Gr6, 24, E3, 3, 1)
    return None

def find_and_fix_labels(content, expected_prefix):
    """Find and fix incorrect labels"""
    fixes = []

    # Pattern to find labels like Gr6_24_3_1_step_2 (missing E3)
    label_pattern = r'label="(Gr6_\d+)_(\d+)_(\d+)_(step_\d+)"'

    matches = re.finditer(label_pattern, content)
    for match in matches:
        full_label = match.group(0)  # Full label="..."
        grade_week = match.group(1)  # Gr6_24
        variation = match.group(2)   # 3
        step_num = match.group(3)    # 1
        step_part = match.group(4)   # step_2

        # Extract expected parts from filename
        expected_parts = expected_prefix.split('_')
        if len(expected_parts) >= 5:  # Gr6, 24, E3, 3, 1
            expected_grade_week = f"{expected_parts[0]}_{expected_parts[1]}"
            expected_exercise = expected_parts[2]
            expected_variation = expected_parts[3]
            expected_step_num = expected_parts[4]

            # If the label matches the pattern but is missing the exercise identifier
            if (grade_week == expected_grade_week and
                variation == expected_variation and
                step_num == expected_step_num):

                # This label is missing the exercise identifier
                correct_label = f'label="{grade_week}_{expected_exercise}_{variation}_{step_num}_{step_part}"'
                fixes.append((full_label, correct_label))

    return fixes

def process_html_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # Extract expected prefix from filename
        filename = filepath.name
        exercise_info = extract_exercise_info_from_filename(filename)

        if not exercise_info:
            return False, []

        grade, week, exercise, variation, step = exercise_info
        expected_prefix = f"{grade}_{week}_{exercise}_{variation}_{step}"

        # Find and fix incorrect labels
        label_fixes = find_and_fix_labels(content, expected_prefix)

        for old_label, new_label in label_fixes:
            content = content.replace(old_label, new_label)
            changes.append(f"    {old_label} -> {new_label}")

        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes

        return False, []

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, []

def main():
    html_dir = Path("html")

    if not html_dir.exists():
        print("ERROR: html directory does not exist!")
        return

    print("HTML Label Issues Fix Script")
    print("=" * 50)

    total_files_checked = 0
    total_files_changed = 0
    all_changes = []

    # Process each target exercise
    for exercise_id in TARGET_EXERCISES:
        print(f"\nProcessing {exercise_id}...")

        # Find all HTML files matching this exercise pattern
        pattern = f"{exercise_id}_*.html"
        matching_files = list(html_dir.glob(pattern))

        if not matching_files:
            print(f"  No HTML files found for {exercise_id}")
            continue

        exercise_files_changed = 0
        exercise_changes = []

        for html_file in sorted(matching_files):
            total_files_checked += 1
            was_changed, changes = process_html_file(html_file)

            if was_changed:
                total_files_changed += 1
                exercise_files_changed += 1

                file_info = f"{html_file.name}"
                all_changes.append((file_info, changes))
                exercise_changes.append((file_info, changes))

                print(f"  FIXED {html_file.name}")
                for change in changes:
                    print(change)

        if exercise_files_changed == 0:
            print(f"  No changes needed for {exercise_id}")
        else:
            print(f"  {exercise_id}: {exercise_files_changed} files fixed")

    # Print summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE FIX REPORT")
    print("=" * 80)
    print(f"Total files checked: {total_files_checked}")
    print(f"Total files changed: {total_files_changed}")
    print(f"Total exercises processed: {len(TARGET_EXERCISES)}")

    if all_changes:
        print(f"\nDETAILED CHANGES ({len(all_changes)} files):")
        print("-" * 50)

        for i, (filename, changes) in enumerate(all_changes, 1):
            print(f"{i:2d}. {filename}")
            for change in changes:
                print(f"  {change}")
            print()
    else:
        print("\nNo changes were needed - all labels were already correct!")

    print("=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()