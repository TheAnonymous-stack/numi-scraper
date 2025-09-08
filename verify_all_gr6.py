import json
import glob
import re
import os

# Get ALL Grade 6 variation files
all_files = sorted(glob.glob('Gr6_*_variations.json'))
print(f'COMPLETE VERIFICATION OF ALL {len(all_files)} GRADE 6 FILES')
print('=' * 80)

# Organize by week
by_week = {}
for file_path in all_files:
    match = re.search(r'Gr6_(\d+)_E(\d+)_variations\.json', os.path.basename(file_path))
    if match:
        week = int(match.group(1))
        if week not in by_week:
            by_week[week] = []
        by_week[week].append(file_path)

# Check EVERY SINGLE FILE
total_ok = 0
total_error = 0

for week in sorted(by_week.keys()):
    print(f'\nWEEK {week}:')
    print('-' * 40)
    
    for file_path in sorted(by_week[week]):
        filename = os.path.basename(file_path)
        match = re.search(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
        exercise_num = match.group(2)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        variations = data if isinstance(data, list) else data.get('variations', [])
        
        # Get first, middle, and last variation details
        first = variations[0] if variations else {}
        middle = variations[25] if len(variations) > 25 else {}
        last = variations[-1] if variations else {}
        
        # Check if format is correct
        format_ok = True
        for i, v in enumerate(variations, 1):
            expected = f'{exercise_num}_{i}'
            actual = v.get('question_number', '')
            if actual != expected:
                format_ok = False
                break
        
        if len(variations) == 51 and format_ok:
            status = 'OK'
            total_ok += 1
        else:
            status = 'ERROR'
            total_error += 1
        
        print(f'  {filename}: {len(variations)} vars | 1st={first.get("question_number", "?")} | 26th={middle.get("question_number", "?")} | 51st={last.get("question_number", "?")} | [{status}]')

print('\n' + '=' * 80)
print(f'SUMMARY: {total_ok} OK, {total_error} ERROR out of {len(all_files)} total files')
if total_error == 0:
    print('ALL FILES ARE PERFECTLY FORMATTED!')