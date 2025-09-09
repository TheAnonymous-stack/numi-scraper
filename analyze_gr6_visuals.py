import json
import glob
import os

# Get all Grade 6 JSON files
json_files = glob.glob("Gr6_*_variations.json")
json_files.sort()

total_questions_with_visuals = 0
files_to_generate = []

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
        print(f"Unexpected structure in {json_file}")
        continue
    
    # Check each question in the file
    for q_num, question in enumerate(questions, 1):
        has_visual = False
        visual_info = {}
        
        # Check for image_tag
        if 'image_tag' in question and question['image_tag']:
            has_visual = True
            visual_info['image_tag'] = question.get('backend_description', '')
            
        # Check for solution_image_tag
        if 'solution_image_tag' in question and question['solution_image_tag']:
            has_visual = True
            visual_info['solution_image_tag'] = question.get('solution_image_tag', [])
            
        # Check for image_choice_tags
        if 'image_choice_tags' in question and question['image_choice_tags']:
            has_visual = True
            visual_info['image_choice_tags'] = question.get('image_choice_tags', [])
            visual_info['image_choice_descriptions'] = question.get('image_choice_tags_backend_description', [])
            
        # Check for shape_image_tags
        if 'shape_image_tags' in question and question['shape_image_tags']:
            has_visual = True
            visual_info['shape_image_tags'] = question.get('shape_image_tags', [])
        
        if has_visual:
            total_questions_with_visuals += 1
            html_filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}.html"
            files_to_generate.append({
                'filename': html_filename,
                'json_file': json_file,
                'question_num': q_num,
                'visual_info': visual_info,
                'question': question
            })

print(f"Total JSON files: {len(json_files)}")
print(f"Total questions needing visuals: {total_questions_with_visuals}")
print(f"\nFirst 10 files to generate:")
for file_info in files_to_generate[:10]:
    print(f"  {file_info['filename']} from {file_info['json_file']}")
    if 'image_tag' in file_info['visual_info']:
        print(f"    -> image_tag: {file_info['visual_info']['image_tag'][:100]}...")

# Save list for processing
with open('gr6_files_to_generate.json', 'w') as f:
    json.dump(files_to_generate, f, indent=2)

print(f"\nFull list saved to gr6_files_to_generate.json")