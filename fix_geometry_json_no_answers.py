import json
import os
import re

def fix_json_questions(json_file):
    """Update JSON files to add context without revealing answers"""
    if not os.path.exists(json_file):
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    
    for quiz in data['quizzes']:
        backend_desc = quiz.get('backend_description', '')
        question_text = quiz.get('question_text', '')
        
        # For Gr6_51_E1 and similar - polygon angle problems
        if 'Gr6_51_E1' in json_file or 'Gr6_51_E4' in json_file:
            # Extract all angle values from backend description
            angle_pattern = r'(\d+)°'
            angles = re.findall(angle_pattern, backend_desc)
            
            # Find variable name
            var_match = re.search(r'variable\s+(\w+)', backend_desc)
            variable = var_match.group(1) if var_match else 'x'
            
            # Extract polygon type
            polygon_types = {
                'triangle': 'triangle',
                'quadrilateral': 'quadrilateral', 
                'pentagon': 'pentagon',
                'hexagon': 'hexagon',
                'heptagon': 'heptagon',
                'octagon': 'octagon',
                'nonagon': 'nonagon',
                'decagon': 'decagon',
                'dodecagon': 'dodecagon'
            }
            
            shape = 'polygon'
            for key, val in polygon_types.items():
                if key in backend_desc.lower():
                    shape = val
                    break
            
            if angles and len(angles) > 1:
                # Create question with some angle values but not the answer
                # Show all angles except don't reveal which one is missing
                angles_shown = angles[:-1]  # Show all but last angle
                if len(angles_shown) > 3:
                    angles_str = ', '.join(angles_shown[:3]) + '°, ...'
                else:
                    angles_str = ', '.join(angles_shown) + '°'
                
                new_question = f"The {shape} has interior angles including {angles_str} and one unknown angle {variable}.\nWhat is {variable}?\n{variable} = ___°"
                quiz['question_text'] = new_question
                modified = True
        
        # For Gr6_50_E1 and E2 - protractor questions
        elif 'Gr6_50' in json_file:
            # Just ask to measure the angle without revealing the answer
            new_question = "What is the measurement of the angle shown on the protractor?\n___°"
            quiz['question_text'] = new_question
            modified = True
        
        # For Gr6_51_E2 - exterior angles
        elif 'Gr6_51_E2' in json_file:
            # Extract polygon type for context
            polygon_types = {
                'triangle': 'triangle',
                'quadrilateral': 'quadrilateral',
                'pentagon': 'pentagon', 
                'hexagon': 'hexagon',
                'heptagon': 'heptagon',
                'octagon': 'octagon',
                'nonagon': 'nonagon',
                'decagon': 'decagon'
            }
            
            shape = 'convex polygon'
            for key, val in polygon_types.items():
                if key in backend_desc.lower():
                    shape = val
                    break
            
            new_question = f"The diagram shows a {shape}.\nWhat is the sum of the exterior angle measures, one at each vertex?\n___°"
            quiz['question_text'] = new_question
            modified = True
        
        # For Gr6_51_E3 - complementary/supplementary angles
        elif 'Gr6_51_E3' in json_file:
            # Keep the existing question format as it doesn't reveal answers
            pass
        
        # For Gr6_52_E1 - trapezoid cutting
        elif 'Gr6_52_E1' in json_file:
            new_question = "Maggie cuts a trapezoid along a vertical dashed line through the middle. Which two shapes does she make?"
            quiz['question_text'] = new_question
            modified = True
    
    if modified:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {json_file}")
    
    return modified

def main():
    """Fix all geometry JSON files"""
    json_files = [
        'Gr6_50_E1_variations.json',
        'Gr6_50_E2_variations.json', 
        'Gr6_51_E1_variations.json',
        'Gr6_51_E2_variations.json',
        'Gr6_51_E3_variations.json',
        'Gr6_51_E4_variations.json',
        'Gr6_52_E1_variations.json'
    ]
    
    print("Fixing JSON files to remove answers from questions...")
    for json_file in json_files:
        fix_json_questions(json_file)
    
    print("\nDone! JSON files updated with context but no answers revealed.")

if __name__ == "__main__":
    main()