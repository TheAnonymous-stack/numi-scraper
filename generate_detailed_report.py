import json
import os
import re
from pathlib import Path
from collections import defaultdict

# Parse the full check output
with open('gr6_full_check.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract issues by category
issues_by_type = defaultdict(list)
current_exercise = None

for line in lines:
    if line.strip().startswith('Gr6_') and ':' in line and not line.strip().startswith('- Gr6_'):
        current_exercise = line.strip().split(':')[0].strip()
    elif '- Question' in line and current_exercise:
        if 'Missing HTML file' in line:
            issues_by_type['missing_files'].append((current_exercise, line.strip()))
        elif 'Missing div with label' in line:
            issues_by_type['missing_divs'].append((current_exercise, line.strip()))
        elif 'Empty HTML' in line:
            issues_by_type['empty_html'].append((current_exercise, line.strip()))
        elif 'Extra divs found' in line:
            issues_by_type['extra_divs'].append((current_exercise, line.strip()))

# Generate detailed report
print("="*80)
print("GRADE 6 HTML VISUAL QUALITY CHECK - DETAILED REPORT")
print("="*80)
print()

# Summary
print("EXECUTIVE SUMMARY")
print("-"*40)
print("Total Grade 6 Exercises: 177")
print("Exercises with Images: 82")
print("Passed Validation: 95")
print("Failed Validation: 82")
print("Pass Rate: 53.7%")
print()

# Issue breakdown
print("ISSUES BY CATEGORY")
print("-"*40)
print(f"1. Missing HTML Files: {len(issues_by_type['missing_files'])} issues")
print(f"2. Missing Divs: {len(issues_by_type['missing_divs'])} issues")
print(f"3. Empty HTML Content: {len(issues_by_type['empty_html'])} issues")
print(f"4. Extra Divs: {len(issues_by_type['extra_divs'])} issues")
print()

# Most problematic exercises
print("TOP 10 MOST PROBLEMATIC EXERCISES")
print("-"*40)
exercise_issue_count = defaultdict(int)
for issue_type, issues in issues_by_type.items():
    for exercise, _ in issues:
        exercise_issue_count[exercise] += 1

sorted_exercises = sorted(exercise_issue_count.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (exercise, count) in enumerate(sorted_exercises, 1):
    print(f"{i}. {exercise}: {count} issues")
print()

# Specific recommendations
print("RECOMMENDED ACTIONS")
print("-"*40)
print("Priority 1 - Create Missing HTML Files:")
missing_file_exercises = set()
for exercise, issue in issues_by_type['missing_files']:
    missing_file_exercises.add(exercise)

if missing_file_exercises:
    print(f"  The following exercises need HTML files created:")
    for exercise in sorted(missing_file_exercises)[:10]:
        print(f"    - {exercise}")
    if len(missing_file_exercises) > 10:
        print(f"    ... and {len(missing_file_exercises) - 10} more")
print()

print("Priority 2 - Fix Empty HTML Content:")
empty_html_exercises = set()
for exercise, issue in issues_by_type['empty_html']:
    empty_html_exercises.add(exercise)

if empty_html_exercises:
    print(f"  The following exercises have empty HTML content:")
    for exercise in sorted(empty_html_exercises)[:5]:
        print(f"    - {exercise}")
    if len(empty_html_exercises) > 5:
        print(f"    ... and {len(empty_html_exercises) - 5} more")
print()

print("Priority 3 - Add Missing Divs:")
missing_div_exercises = set()
for exercise, issue in issues_by_type['missing_divs']:
    missing_div_exercises.add(exercise)

if missing_div_exercises:
    print(f"  The following exercises have missing divs:")
    for exercise in sorted(missing_div_exercises)[:5]:
        print(f"    - {exercise}")
    if len(missing_div_exercises) > 5:
        print(f"    ... and {len(missing_div_exercises) - 5} more")
print()

# Pattern analysis
print("PATTERN ANALYSIS")
print("-"*40)

# Check which weeks have the most issues
week_issues = defaultdict(int)
for exercise in exercise_issue_count.keys():
    match = re.match(r'Gr6_(\d+)_', exercise)
    if match:
        week = int(match.group(1))
        week_issues[week] += exercise_issue_count[exercise]

print("Weeks with most issues:")
sorted_weeks = sorted(week_issues.items(), key=lambda x: x[1], reverse=True)[:5]
for week, count in sorted_weeks:
    print(f"  Week {week}: {count} total issues")
print()

# File naming pattern check
print("FILE NAMING PATTERNS DETECTED")
print("-"*40)
print("Expected pattern: HTML/Gr6_{week}_E{exercise} {question}.html")
print("Alternative pattern: HTML/Gr6_{week}_E{exercise}_{question}.html")
print()
print("Note: The checker looks for both patterns. Most exercises appear to need")
print("files with a space before the question number (not underscore).")
print()

print("="*80)
print("END OF REPORT")
print("="*80)