import json
import re

def extract_dimensions_from_backend(backend_description):
    """Extract rectangle dimensions from backend description"""
    # Look for patterns like "measures X unit wide and Y unit tall"
    pattern = r'measures (\d+) (\w+) wide and (\d+) (\w+) tall'
    matches = list(re.finditer(pattern, backend_description))
    
    if len(matches) >= 2:
        # First rectangle (larger)
        width1 = matches[0].group(1)
        unit1 = matches[0].group(2)
        height1 = matches[0].group(3)
        
        # Second rectangle (smaller)
        width2 = matches[1].group(1) 
        unit2 = matches[1].group(2)
        height2 = matches[1].group(3)
        
        return width1, height1, width2, height2, unit1
    return None

def process_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract dimensions from backend description
            dimensions = extract_dimensions_from_backend(quiz['backend_description'])
            
            if dimensions:
                width1, height1, width2, height2, unit = dimensions
                
                # Create new question text with dimensions
                if unit in quiz['question_text']:
                    unit_word = f"square {unit}"
                else:
                    unit_word = "square units"
                
                new_question = f"This compound figure is made up of two rectangles joined together.\n"
                new_question += f"The larger rectangle measures {width1} {unit} wide and {height1} {unit} tall.\n"
                new_question += f"The smaller rectangle measures {width2} {unit} wide and {height2} {unit} tall.\n"
                new_question += f"What is the area of this figure?\n___ {unit_word}"
                
                quiz['question_text'] = new_question
        
        # Remove image-related fields
        if 'image_tag' in quiz:
            del quiz['image_tag']
        if 'backend_description' in quiz:
            del quiz['backend_description']
        if 'solution_image_tag' in quiz:
            del quiz['solution_image_tag']
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Processed {filename} - removed images and added dimensions to question text")

# Process the file
process_file('Gr6_52_E4_variations.json')
print("Done!")