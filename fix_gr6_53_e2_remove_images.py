import json
import re

def extract_cube_info_from_backend(backend_description):
    """Extract cube side length and unit from backend description"""
    # Pattern to match: "This image shows a cube with each side labeled as X Y."
    pattern = r'This image shows a cube with each side labeled as (\d+) (\w+)'
    match = re.search(pattern, backend_description)
    
    if match:
        side_length = match.group(1)
        unit = match.group(2)
        return side_length, unit
    
    return None, None

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract cube information from backend description
            side_length, unit = extract_cube_info_from_backend(quiz['backend_description'])
            
            if side_length and unit:
                # Update question text to include the cube information
                original_question = quiz['question_text']
                
                # Add cube information before the question
                new_question = f"A cube has sides that are {side_length} {unit} long.\\n{original_question}"
                
                quiz['question_text'] = new_question
        
        # Remove image-related fields
        if 'image_tag' in quiz:
            del quiz['image_tag']
        if 'backend_description' in quiz:
            del quiz['backend_description']
        if 'solution_image_tag' in quiz:
            del quiz['solution_image_tag']
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {filename} - removed images and added cube information to question text")

# Process the file
process_file('Gr6_53_E2_variations.json')
print("Done!")