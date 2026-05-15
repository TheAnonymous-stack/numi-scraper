import json
import re

def extract_triangular_prism_info_from_backend(backend_description):
    """Extract triangular prism dimensions from backend description"""
    # Pattern to match: "triangular bases having base X Y and height Z W. The prism length is A B."
    pattern = r'triangular bases having base (\d+) (\w+) and height (\d+) (\w+)\. The prism length is (\d+) (\w+)'
    match = re.search(pattern, backend_description)
    
    if match:
        base = match.group(1)
        base_unit = match.group(2)
        height = match.group(3)
        height_unit = match.group(4)
        length = match.group(5)
        length_unit = match.group(6)
        
        # Assuming all units are the same (which they should be)
        unit = base_unit
        return base, height, length, unit
    
    return None, None, None, None

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract triangular prism information from backend description
            base, height, length, unit = extract_triangular_prism_info_from_backend(quiz['backend_description'])
            
            if base and height and length and unit:
                # Update question text to include the triangular prism information
                original_question = quiz['question_text']
                
                # Add triangular prism information before the question
                new_question = f"A triangular prism has triangular bases with base {base} {unit} and height {height} {unit}. The prism length is {length} {unit}.\\n{original_question}"
                
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
    
    print(f"Processed {filename} - removed images and added triangular prism information to question text")

# Process the file
process_file('Gr6_53_E3_variations.json')
print("Done!")