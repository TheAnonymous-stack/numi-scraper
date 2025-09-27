#!/usr/bin/env python3
"""
Script to fix question numbering in Grade 7 JSON files.

This script:
1. Identifies all Gr7_*_E*_variations.json files with numbering issues
2. Extracts the exercise number from the filename (E1 -> 1, E2 -> 2, etc.)
3. Renumbers questions to follow the pattern {exercise}_{1-51}
4. Ensures each file has exactly 51 variations

Example: For Gr7_10_E2_variations.json, questions should be numbered 2_1, 2_2, ..., 2_51
"""

import json
import os
import re
import glob
from pathlib import Path

def extract_exercise_number(filename):
    """Extract exercise number from filename like Gr7_10_E2_variations.json -> 2"""
    match = re.search(r'_E(\d+)_variations\.json$', filename)
    if match:
        return int(match.group(1))
    return None

def check_file_needs_fixing(filepath):
    """Check if a file has numbering issues"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'quizzes' not in data:
            return False, "No quizzes field found"

        quizzes = data['quizzes']
        if len(quizzes) == 0:
            return False, "No quizzes in file"

        # Extract exercise number from filename
        exercise_num = extract_exercise_number(filepath)
        if exercise_num is None:
            return False, "Could not extract exercise number"

        # Check if we have exactly 51 questions
        expected_count = 51
        actual_count = len(quizzes)

        # Check first and last question numbers
        first_question = quizzes[0].get('question_number', '')
        last_question = quizzes[-1].get('question_number', '')

        expected_first = f"{exercise_num}_1"
        expected_last = f"{exercise_num}_51"

        needs_fixing = False
        issues = []

        if actual_count != expected_count:
            needs_fixing = True
            issues.append(f"Expected {expected_count} questions, found {actual_count}")

        if first_question != expected_first:
            needs_fixing = True
            issues.append(f"First question is '{first_question}', expected '{expected_first}'")

        if last_question != expected_last:
            needs_fixing = True
            issues.append(f"Last question is '{last_question}', expected '{expected_last}'")

        return needs_fixing, "; ".join(issues) if issues else "No issues"

    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def fix_file_numbering(filepath):
    """Fix the question numbering in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'quizzes' not in data:
            return False, "No quizzes field found"

        quizzes = data['quizzes']
        exercise_num = extract_exercise_number(filepath)

        if exercise_num is None:
            return False, "Could not extract exercise number"

        # Renumber all questions
        for i, quiz in enumerate(quizzes, 1):
            quiz['question_number'] = f"{exercise_num}_{i}"

        # Ensure we have exactly 51 questions
        if len(quizzes) > 51:
            # Trim to 51 questions
            data['quizzes'] = quizzes[:51]
        elif len(quizzes) < 51:
            return False, f"File has only {len(quizzes)} questions, cannot extend to 51"

        # Write back the fixed file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return True, "Fixed successfully"

    except Exception as e:
        return False, f"Error fixing file: {str(e)}"

def main():
    """Main function to identify and fix all problematic files"""
    # Find all Grade 7 JSON files
    pattern = "Gr7_*_E*_variations.json"
    files = glob.glob(pattern)

    print(f"Found {len(files)} Grade 7 JSON files")
    print()

    # Check each file for issues
    files_to_fix = []
    for filepath in sorted(files):
        needs_fixing, reason = check_file_needs_fixing(filepath)
        if needs_fixing:
            files_to_fix.append((filepath, reason))
            print(f"NEEDS FIXING: {os.path.basename(filepath)}")
            print(f"  Reason: {reason}")
        else:
            print(f"OK: {os.path.basename(filepath)}")

    print(f"\nSummary: {len(files_to_fix)} files need fixing out of {len(files)} total files")

    if not files_to_fix:
        print("No files need fixing!")
        return

    # Show files that will be fixed
    print(f"\nFiles that will be fixed:")
    for filepath, reason in files_to_fix:
        print(f"  - {os.path.basename(filepath)}: {reason}")

    print(f"\nProceeding to fix {len(files_to_fix)} files automatically...")

    # Fix each problematic file
    print("\nFixing files...")
    fixed_count = 0
    for filepath, _ in files_to_fix:
        success, message = fix_file_numbering(filepath)
        if success:
            fixed_count += 1
            print(f"[OK] Fixed: {os.path.basename(filepath)}")
        else:
            print(f"[ERROR] Failed to fix {os.path.basename(filepath)}: {message}")

    print(f"\nCompleted: {fixed_count}/{len(files_to_fix)} files fixed successfully")

    # Final verification
    print("\nVerifying fixes...")
    verification_passed = 0
    for filepath, _ in files_to_fix:
        needs_fixing, reason = check_file_needs_fixing(filepath)
        if not needs_fixing:
            verification_passed += 1
            print(f"[OK] Verified: {os.path.basename(filepath)}")
        else:
            print(f"[ERROR] Still has issues: {os.path.basename(filepath)} - {reason}")

    print(f"\nFinal result: {verification_passed}/{len(files_to_fix)} files verified as fixed")

if __name__ == "__main__":
    main()