import json
import re

def extract_pyramid_info_from_backend(backend_description):
    """Extract rectangular pyramid dimensions from backend description"""
    # Pattern to match: "square base of X Y by Z W. Each triangular face has a base of A B and a slant height of C D."
    pattern = r'square base of (\d+) (\w+) by (\d+) (\w+)\. Each triangular face has a base of (\d+) (\w+) and a slant height of (\d+) (\w+)'
    match = re.search(pattern, backend_description)
    
    if match:
        base_side1 = match.group(1)
        base_unit1 = match.group(2)
        base_side2 = match.group(3)
        base_unit2 = match.group(4)
        tri_base = match.group(5)
        tri_base_unit = match.group(6)
        slant_height = match.group(7)
        slant_unit = match.group(8)
        
        # Assuming all units are the same (which they should be) and base is square
        unit = base_unit1
        base_side = base_side1  # Since it's a square base
        return base_side, slant_height, unit
    
    return None, None, None

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract pyramid information from backend description
            base_side, slant_height, unit = extract_pyramid_info_from_backend(quiz['backend_description'])
            
            if base_side and slant_height and unit:
                # Update question text to include the pyramid information
                original_question = quiz['question_text']
                
                # Add pyramid information before the question
                new_question = f"A rectangular pyramid has a square base of {base_side} {unit} by {base_side} {unit}. Each triangular face has a base of {base_side} {unit} and a slant height of {slant_height} {unit}.\\n{original_question}"
                
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
    
    print(f"Processed {filename} - removed images and added rectangular pyramid information to question text")

# Process the file
process_file('Gr6_53_E4_variations.json')
print("Done!")