#!/usr/bin/env python3
"""
Fix label attribute mismatches in Grade 6 HTML files.
The issue: label attributes reference variation numbers that are off by +1.
For example, Gr6_24_E3_3_1.html has label="Gr6_24_3_2_step_2" when it should be label="Gr6_24_3_1_step_2"
"""

import os
import re
import glob
from typing import List, Tuple, Dict

# List of exercises that need fixing
PROBLEMATIC_EXERCISES = [
    'Gr6_54_E3', 'Gr6_55_E1', 'Gr6_1_E4', 'Gr6_1_E5', 'Gr6_2_E1', 'Gr6_3_E4', 'Gr6_5_E1',
    'Gr6_3_E2', 'Gr6_15_E5', 'Gr6_16_E1', 'Gr6_23_E1', 'Gr6_23_E2', 'Gr6_23_E3', 'Gr6_24_E1',
    'Gr6_24_E2', 'Gr6_24_E3', 'Gr6_28_E3', 'Gr6_33_E1', 'Gr6_33_E2', 'Gr6_34_E3', 'Gr6_35_E1',
    'Gr6_36_E1', 'Gr6_42_E4', 'Gr6_43_E2', 'Gr6_44_E1', 'Gr6_44_E2', 'Gr6_44_E3', 'Gr6_45_E2',
    'Gr6_45_E4', 'Gr6_50_E1', 'Gr6_50_E2', 'Gr6_51_E1', 'Gr6_51_E2', 'Gr6_51_E3', 'Gr6_51_E4',
    'Gr6_52_E1', 'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_48_E1'
]

def extract_variation_from_filename(filename: str) -> Tuple[str, int]:
    """
    Extract the exercise prefix and variation number from filename.
    e.g., 'Gr6_24_E3_3_1.html' -> ('Gr6_24_E3_3', 1)
    """
    # Remove .html extension
    name = os.path.basename(filename).replace('.html', '')

    # Pattern: Gr6_X_EY_Z_N where N is the variation number
    match = re.match(r'^(Gr6_\d+_E\d+_\d+)_(\d+)$', name)
    if match:
        prefix = match.group(1)
        variation = int(match.group(2))
        return prefix, variation
    else:
        raise ValueError(f"Could not parse filename: {filename}")

def find_html_files_for_exercises(html_dir: str) -> Dict[str, List[str]]:
    """
    Find all HTML files for the problematic exercises.
    Returns dict mapping exercise -> list of HTML files
    """
    exercise_files = {}

    for exercise in PROBLEMATIC_EXERCISES:
        # Convert exercise name to pattern (e.g., Gr6_24_E3 -> Gr6_24_E3_*)
        pattern = os.path.join(html_dir, f"{exercise}_*.html")
        files = glob.glob(pattern)

        if files:
            exercise_files[exercise] = sorted(files)

    return exercise_files

def fix_label_in_content(content: str, correct_variation: int) -> Tuple[str, int]:
    """
    Fix label attributes in HTML content.
    Returns (fixed_content, number_of_fixes)
    """
    fixes_made = 0

    # Pattern to match label attributes with step references
    # e.g., label="Gr6_24_3_2_step_5" should become label="Gr6_24_3_1_step_5" for variation 1
    step_pattern = r'label="(Gr6_\d+_\d+)_(\d+)((?:_step_\d+))"'

    def replace_step_label(match):
        nonlocal fixes_made
        prefix = match.group(1)  # e.g., "Gr6_24_3"
        old_variation = int(match.group(2))  # e.g., 2
        suffix = match.group(3)  # e.g., "_step_5"

        # Fix: replace old variation with correct variation
        new_label = f'label="{prefix}_{correct_variation}{suffix}"'
        fixes_made += 1
        print(f"    Fixing: {match.group(0)} -> {new_label}")
        return new_label

    content = re.sub(step_pattern, replace_step_label, content)

    return content, fixes_made

def fix_html_file(filepath: str) -> int:
    """
    Fix label mismatches in a single HTML file.
    Returns number of fixes made.
    """
    try:
        # Extract variation number from filename
        _, variation = extract_variation_from_filename(filepath)

        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix labels
        fixed_content, fixes_made = fix_label_in_content(content, variation)

        if fixes_made > 0:
            # Write back fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  Fixed {fixes_made} labels in {os.path.basename(filepath)}")
        else:
            print(f"  No fixes needed in {os.path.basename(filepath)}")

        return fixes_made

    except Exception as e:
        print(f"  ERROR fixing {filepath}: {e}")
        return 0

def main():
    """Main function to fix all label mismatches."""
    html_dir = os.path.join(os.getcwd(), 'html')

    if not os.path.exists(html_dir):
        print(f"ERROR: HTML directory not found: {html_dir}")
        return

    print("Starting Grade 6 HTML label mismatch fix...")
    print(f"Looking for HTML files in: {html_dir}")
    print(f"Problematic exercises to fix: {len(PROBLEMATIC_EXERCISES)}")

    # Find all HTML files for problematic exercises
    exercise_files = find_html_files_for_exercises(html_dir)

    total_files = 0
    total_fixes = 0
    modified_files = []

    for exercise, files in exercise_files.items():
        print(f"\nProcessing {exercise}: {len(files)} files")

        for filepath in files:
            fixes = fix_html_file(filepath)
            total_files += 1
            total_fixes += fixes

            if fixes > 0:
                modified_files.append(filepath)

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Total files modified: {len(modified_files)}")
    print(f"Total label fixes made: {total_fixes}")

    if modified_files:
        print(f"\nModified files:")
        for filepath in sorted(modified_files):
            print(f"  {os.path.basename(filepath)}")

    print("\nDone!")

if __name__ == "__main__":
    main()