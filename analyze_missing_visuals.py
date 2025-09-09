import json
import glob
import os

# Get all Grade 6 JSON files
json_files = glob.glob("Gr6_*_variations.json")
json_files.sort()

# Get all existing HTML files
html_files = set(glob.glob("Gr6_*.html"))

missing_files = []
existing_files = []

for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract week and exercise from filename
    parts = os.path.basename(json_file).replace("_variations.json", "").split("_")
    week = parts[1]
    exercise = parts[2]
    
    # Check if data is a dict with 'quizzes' key or a list
    if isinstance(data, dict) and 'quizzes' in data:
        questions = data['quizzes']
    elif isinstance(data, list):
        questions = data
    else:
        continue
    
    # Check each question in the file
    for q_num, question in enumerate(questions, 1):
        has_visual = False
        
        # Check for any visual fields
        if ('image_tag' in question and question['image_tag']) or \
           ('solution_image_tag' in question and question['solution_image_tag']) or \
           ('image_choice_tags' in question and question['image_choice_tags']) or \
           ('shape_image_tags' in question and question['shape_image_tags']):
            has_visual = True
        
        if has_visual:
            html_filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}.html"
            full_path = os.path.join(os.getcwd(), html_filename)
            
            if html_filename in [os.path.basename(f) for f in html_files]:
                existing_files.append(html_filename)
            else:
                missing_files.append({
                    'filename': html_filename,
                    'json_file': json_file,
                    'question_num': q_num
                })

print(f"Total existing HTML files: {len(existing_files)}")
print(f"Total missing HTML files: {len(missing_files)}")

if missing_files:
    print("\nFirst 10 missing files:")
    for file_info in missing_files[:10]:
        print(f"  {file_info['filename']} from {file_info['json_file']}")
else:
    print("\nAll required HTML files have been generated!")