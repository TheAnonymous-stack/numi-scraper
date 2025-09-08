import json
import glob
import os
import re

def fix_variation_file(file_path):
    """Fix all issues in a single variation file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract exercise number from filename
    match = re.search(r'Gr6_\d+_E(\d+)_variations\.json', os.path.basename(file_path))
    if not match:
        print(f"Could not extract exercise number from {file_path}")
        return False
    
    exercise_number = match.group(1)
    
    # Process each variation
    fixed_variations = []
    for i, variation in enumerate(data, 1):
        # Fix question_number format
        variation['question_number'] = f"{exercise_number}_{i}"
        
        # Fix question_type "Multiple Fill in the blank" -> "Multiple fill in the blank"
        if variation.get('question_type') == 'Multiple Fill in the blank':
            variation['question_type'] = 'Multiple fill in the blank'
        
        # Fix "Fraction Fill in the blank" and "Fractions Fill in the blank" questions
        if variation.get('question_type') in ['Fraction Fill in the blank', 'Fractions Fill in the blank']:
            variation['question_type'] = 'Multiple fill in the blank'
            # Ensure question_text has proper format for mixed numbers
            if '_ _/_' not in variation.get('question_text', ''):
                # Add the format if not present (this may need adjustment based on actual content)
                pass
            # Ensure orderMatter is True for fraction questions
            variation['orderMatter'] = True
        
        # Fix correct_answers format based on question_type
        if 'correct_answers' in variation:
            correct_answers = variation['correct_answers']
            
            if variation.get('question_type') in ['Fill in the blank', 'Multiple fill in the blank']:
                # Remove unnecessary nested layers
                # If it's a list of lists with single elements, flatten it
                if isinstance(correct_answers, list):
                    flattened = []
                    for answer in correct_answers:
                        if isinstance(answer, list):
                            # If it's a nested list with only one element, flatten it
                            if len(answer) == 1 and not isinstance(answer[0], list):
                                flattened.append(answer[0])
                            # If it's a nested list with multiple elements (alternate answers), keep nested
                            elif len(answer) > 1:
                                flattened.append(answer)
                            else:
                                flattened.extend(answer)
                        else:
                            flattened.append(answer)
                    
                    # For single answers, ensure it's not nested
                    if len(flattened) == 1 and isinstance(flattened[0], list) and len(flattened[0]) == 1:
                        variation['correct_answers'] = [flattened[0][0]]
                    else:
                        variation['correct_answers'] = flattened
        
        # For Multiple fill in the blank, check if orderMatter should be False
        if variation.get('question_type') == 'Multiple fill in the blank':
            # If orderMatter is not set or needs to be False based on question context
            if 'orderMatter' not in variation:
                # Default to False unless it's a fraction question
                variation['orderMatter'] = False
        
        fixed_variations.append(variation)
    
    # Ensure exactly 51 variations
    current_count = len(fixed_variations)
    if current_count < 51:
        print(f"WARNING: {file_path} has only {current_count} variations, expected 51")
        # You might want to duplicate the last variation or handle this differently
    elif current_count > 51:
        print(f"WARNING: {file_path} has {current_count} variations, truncating to 51")
        fixed_variations = fixed_variations[:51]
    
    # Write back the fixed data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_variations, f, indent=2, ensure_ascii=False)
    
    return True

def main():
    # Find all variation files
    variation_files = glob.glob('Gr6_*_variations.json')
    
    print(f"Found {len(variation_files)} variation files to process")
    
    success_count = 0
    for file_path in variation_files:
        print(f"Processing {file_path}...")
        if fix_variation_file(file_path):
            success_count += 1
    
    print(f"\nSuccessfully processed {success_count}/{len(variation_files)} files")

if __name__ == "__main__":
    main()