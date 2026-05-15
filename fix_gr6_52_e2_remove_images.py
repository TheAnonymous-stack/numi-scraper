import json
import re

def add_dimensions_to_text(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract dimensions from backend description
            desc = quiz['backend_description']
            
            # Extract the measurements
            bottom_match = re.search(r'bottom base measuring (\d+) (\w+)', desc)
            top_match = re.search(r'top base measuring (\d+) (\w+)', desc)
            height_match = re.search(r'height labeled as (\d+) (\w+)', desc)
            
            if bottom_match and top_match and height_match:
                bottom_base = bottom_match.group(1)
                top_base = top_match.group(1)
                height = height_match.group(1)
                unit = bottom_match.group(2)
                
                # Update question text with dimensions
                if "What is the area?" in quiz['question_text']:
                    quiz['question_text'] = f"A trapezoid has bases of {top_base} {unit} and {bottom_base} {unit}, and a height of {height} {unit}.\\nWhat is the area?\\n___ square {unit}"
                
                # Remove image-related fields
                if 'image_tag' in quiz:
                    del quiz['image_tag']
                if 'backend_description' in quiz:
                    del quiz['backend_description']
                if 'solution_image_tag' in quiz:
                    del quiz['solution_image_tag']
                
                # Update solution to match the new format
                if 'solution' in quiz and len(quiz['solution']) > 0:
                    # Update the first solution step with the correct dimensions
                    quiz['solution'][0][1] = f"Find the bases and height of the trapezoid.\\n$\\text{{base}}_1 = {bottom_base}$ {unit[0]}\\n$\\text{{base}}_2 = {top_base}$ {unit[0]}\\n$\\text{{height}} = {height}$ {unit[0]}"
                    
                    # Update the second solution step with the calculation
                    if len(quiz['solution']) > 1:
                        quiz['solution'][1][1] = f"Use these numbers in the area of a trapezoid formula.\\n$\\text{{Area}} = \\frac{{1}}{{2}} \\times \\text{{height}} \\times (\\text{{base}}_1 + \\text{{base}}_2)$\\n$= \\frac{{1}}{{2}} \\times {height}({bottom_base}+{top_base})$\\n$= {quiz['correct_answers'][0]}$"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Removed images and added dimensions to question text in {filename}")

# Process the file
add_dimensions_to_text('Gr6_52_E2_variations.json')