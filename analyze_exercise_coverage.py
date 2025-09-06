#!/usr/bin/env python3
"""
Script to analyze exercise coverage and identify any gaps.
"""
import glob
import re
from collections import defaultdict

def analyze_exercise_coverage():
    """Analyze exercise coverage to find any gaps."""
    # Find all Grade 6 variation files
    pattern = "Gr6_*_E*_variations.json"
    files = glob.glob(pattern)
    
    # Extract week and exercise numbers
    exercises = defaultdict(list)
    
    for file_path in files:
        # Extract week and exercise number from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', file_path)
        if match:
            week = int(match.group(1))
            exercise = int(match.group(2))
            exercises[week].append(exercise)
    
    # Sort and analyze
    print("Grade 6 Exercise Coverage Analysis")
    print("=" * 50)
    
    total_weeks = len(exercises)
    total_exercises = sum(len(ex_list) for ex_list in exercises.values())
    
    print(f"Total weeks covered: {total_weeks}")
    print(f"Total exercises: {total_exercises}")
    print()
    
    # Check for gaps in weeks
    if exercises:
        min_week = min(exercises.keys())
        max_week = max(exercises.keys())
        
        missing_weeks = []
        for week in range(min_week, max_week + 1):
            if week not in exercises:
                missing_weeks.append(week)
        
        if missing_weeks:
            print(f"Missing weeks: {missing_weeks}")
        else:
            print("No missing weeks found.")
        
        print()
        print("Week-by-Week Breakdown:")
        print("-" * 30)
        
        for week in sorted(exercises.keys()):
            exercise_list = sorted(exercises[week])
            
            # Check for gaps in exercises within the week
            if exercise_list:
                min_ex = min(exercise_list)
                max_ex = max(exercise_list)
                expected = set(range(min_ex, max_ex + 1))
                actual = set(exercise_list)
                missing_exercises = sorted(expected - actual)
                
                status = ""
                if missing_exercises:
                    status = f" (Missing: E{missing_exercises})"
                
                print(f"Week {week:2d}: Exercises {exercise_list}{status}")

if __name__ == "__main__":
    analyze_exercise_coverage()