#!/usr/bin/env python3
"""
Comprehensive HTML Label Fix Script for Grade 6 Exercises

This script fixes HTML label issues where labels in HTML files have incorrect variation numbers
that don't match the filename variation numbers.

The pattern is that HTML files like Gr6_24_E3_3_1.html might have labels like:
- "Gr6_24_3_1_step_2" (missing E3) when it should be "Gr6_24_E3_3_1_step_2"

This script processes only the specified exercises and fixes ALL such label mismatches.
"""

import os
import re
from pathlib import Path

# Target exercises to fix (as specified in the request)
TARGET_EXERCISES = [
    'Gr6_54_E3', 'Gr6_55_E1', 'Gr6_1_E4', 'Gr6_1_E5', 'Gr6_2_E1', 'Gr6_3_E4',
    'Gr6_5_E1', 'Gr6_3_E2', 'Gr6_15_E5', 'Gr6_16_E1', 'Gr6_23_E1', 'Gr6_23_E2',
    'Gr6_23_E3', 'Gr6_24_E1', 'Gr6_24_E2', 'Gr6_24_E3', 'Gr6_28_E3', 'Gr6_33_E1',
    'Gr6_33_E2', 'Gr6_34_E3', 'Gr6_35_E1', 'Gr6_36_E1', 'Gr6_42_E4', 'Gr6_43_E2',
    'Gr6_44_E1', 'Gr6_44_E2', 'Gr6_44_E3', 'Gr6_45_E2', 'Gr6_45_E4', 'Gr6_50_E1',
    'Gr6_50_E2', 'Gr6_51_E1', 'Gr6_51_E2', 'Gr6_51_E3', 'Gr6_51_E4', 'Gr6_52_E1',
    'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_48_E1'
]

class HTMLLabelFixer:
    def __init__(self, html_dir):
        self.html_dir = Path(html_dir)
        self.files_checked = 0
        self.files_changed = 0
        self.changes_made = []

    def extract_exercise_info_from_filename(self, filename):
        """
        Extract exercise info from filename like Gr6_24_E3_3_1.html
        Returns: (grade, week, exercise, variation, step) or None if no match
        """
        pattern = r'^(Gr6)_(\d+)_(E\d+)_(\d+)_(\d+)\.html$'
        match = re.match(pattern, filename)
        if match:
            return match.groups()  # (Gr6, 24, E3, 3, 1)
        return None

    def find_incorrect_labels(self, content, expected_prefix):
        """
        Find labels that are missing the exercise identifier
        Returns list of (old_label, new_label) tuples
        """
        fixes = []

        # Pattern to find labels like Gr6_24_3_1_step_2 (missing E3)
        # We look for labels that match the pattern but are missing the exercise part
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

    def fix_html_file(self, filepath):
        """
        Fix label issues in a single HTML file
        Returns: (was_changed, changes_list)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            changes_in_file = []

            # Extract expected prefix from filename
            filename = filepath.name
            exercise_info = self.extract_exercise_info_from_filename(filename)

            if not exercise_info:
                return False, []

            grade, week, exercise, variation, step = exercise_info
            expected_prefix = f"{grade}_{week}_{exercise}_{variation}_{step}"

            # Find and fix incorrect labels
            label_fixes = self.find_incorrect_labels(content, expected_prefix)

            for old_label, new_label in label_fixes:
                content = content.replace(old_label, new_label)
                changes_in_file.append(f"  {old_label} → {new_label}")

            # Write back if changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes_in_file

            return False, []

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False, []

    def process_exercise(self, exercise_id):
        """
        Process all HTML files for a specific exercise
        """
        print(f"\n=== Processing {exercise_id} ===")

        # Find all HTML files matching this exercise pattern
        pattern = f"{exercise_id}_*.html"
        matching_files = list(self.html_dir.glob(pattern))

        if not matching_files:
            print(f"No HTML files found for {exercise_id}")
            return

        print(f"Found {len(matching_files)} HTML files for {exercise_id}")

        exercise_files_changed = 0
        exercise_changes = []

        for html_file in sorted(matching_files):
            self.files_checked += 1
            was_changed, changes = self.fix_html_file(html_file)

            if was_changed:
                self.files_changed += 1
                exercise_files_changed += 1

                file_change_info = {
                    'file': str(html_file.relative_to(self.html_dir)),
                    'changes': changes
                }
                self.changes_made.append(file_change_info)
                exercise_changes.append(file_change_info)

                print(f"FIXED {html_file.name}")
                for change in changes:
                    print(change)
            else:
                print(f"  {html_file.name} - No changes needed")

        print(f"{exercise_id}: {exercise_files_changed} files changed out of {len(matching_files)} files")

    def run(self):
        """
        Process all target exercises
        """
        print("HTML Label Issues Fix Script")
        print("=" * 50)
        print(f"HTML Directory: {self.html_dir}")
        print(f"Target Exercises: {len(TARGET_EXERCISES)}")

        if not self.html_dir.exists():
            print(f"ERROR: HTML directory {self.html_dir} does not exist!")
            return

        # Process each target exercise
        for exercise_id in TARGET_EXERCISES:
            self.process_exercise(exercise_id)

        self.print_summary()

    def print_summary(self):
        """
        Print comprehensive summary report
        """
        print("\n" + "=" * 80)
        print("COMPREHENSIVE FIX REPORT")
        print("=" * 80)
        print(f"Total files checked: {self.files_checked}")
        print(f"Total files changed: {self.files_changed}")
        print(f"Total exercises processed: {len(TARGET_EXERCISES)}")

        if self.changes_made:
            print(f"\nDETAILED CHANGES ({len(self.changes_made)} files):")
            print("-" * 50)

            for i, change_info in enumerate(self.changes_made, 1):
                print(f"{i:2d}. {change_info['file']}")
                for change in change_info['changes']:
                    print(f"    {change}")
                print()
        else:
            print("\nNo changes were needed - all labels were already correct!")

        # Summary by exercise
        exercise_summary = {}
        for change_info in self.changes_made:
            # Extract exercise from filename
            filename = change_info['file']
            for exercise in TARGET_EXERCISES:
                if filename.startswith(exercise):
                    if exercise not in exercise_summary:
                        exercise_summary[exercise] = 0
                    exercise_summary[exercise] += 1
                    break

        if exercise_summary:
            print("\nCHANGES BY EXERCISE:")
            print("-" * 30)
            for exercise in sorted(exercise_summary.keys()):
                print(f"{exercise}: {exercise_summary[exercise]} files fixed")

        print("\n" + "=" * 80)
        print("VERIFICATION COMPLETE")
        print("=" * 80)

def main():
    script_dir = Path(__file__).parent
    html_dir = script_dir / "html"

    fixer = HTMLLabelFixer(html_dir)
    fixer.run()

if __name__ == "__main__":
    main()