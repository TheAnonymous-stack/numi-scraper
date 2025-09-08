import json
import glob
import os
import re

def fix_correct_answers(correct_answers, question_type):
    """Fix the correct_answers format based on question type"""
    if not isinstance(correct_answers, list):
        return correct_answers
    
    # For Fill in the blank questions
    if question_type == "Fill in the blank":
        # Check if it's unnecessarily nested
        if len(correct_answers) == 1 and isinstance(correct_answers[0], list):
            # If the nested list has only one item, it's not an alternate answer
            if len(correct_answers[0]) == 1:
                return [correct_answers[0][0]]
            else:
                # Multiple items in the nested list means alternate answers, keep it
                return correct_answers
        return correct_answers
    
    # For Multiple fill in the blank questions  
    elif question_type in ["Multiple fill in the blank", "Multiple Fill in the blank"]:
        # If it's a single nested list containing the answers
        if len(correct_answers) == 1 and isinstance(correct_answers[0], list):
            return correct_answers[0]
        
        # Check if each element is unnecessarily nested
        flattened = []
        needs_flattening = False
        for item in correct_answers:
            if isinstance(item, list) and len(item) == 1:
                flattened.append(item[0])
                needs_flattening = True
            else:
                flattened.append(item)
        
        if needs_flattening:
            return flattened
            
        return correct_answers
    
    return correct_answers

def fix_variation_file(file_path):
    """Fix all issues in a single variation file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
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
        
        # Fix "Fraction Fill in the blank" or "Fractions Fill in the blank" questions
        if variation.get('question_type') in ['Fraction Fill in the blank', 'Fractions Fill in the blank']:
            variation['question_type'] = 'Multiple fill in the blank'
            
            # Ensure question_text has proper format for mixed numbers if needed
            question_text = variation.get('question_text', '')
            # Check if we need to add the mixed number format
            if '=_' in question_text and '_ _/_' not in question_text:
                # Check if this looks like a fraction question that needs the format
                if 'mixed number' in question_text.lower() or 'fraction' in question_text.lower():
                    # Replace =_ with =_ _/_
                    variation['question_text'] = question_text.replace('=_', '=_ _/_')
            
            # Ensure orderMatter is True for fraction questions
            variation['orderMatter'] = True
        
        # Fix correct_answers format based on question_type
        if 'correct_answers' in variation:
            original_answers = variation['correct_answers']
            fixed_answers = fix_correct_answers(original_answers, variation.get('question_type', ''))
            variation['correct_answers'] = fixed_answers
        
        # Handle orderMatter for Multiple fill in the blank
        if variation.get('question_type') == 'Multiple fill in the blank':
            # Check if it's a fraction/mixed number question
            question_text = variation.get('question_text', '')
            if '_ _/_' in question_text or 'mixed number' in question_text.lower():
                variation['orderMatter'] = True
            elif 'orderMatter' not in variation:
                # Default to False for non-fraction multiple fill questions
                variation['orderMatter'] = False
        
        fixed_variations.append(variation)
    
    # Ensure exactly 51 variations
    current_count = len(fixed_variations)
    if current_count != 51:
        print(f"WARNING: {file_path} has {current_count} variations instead of 51")
    
    # Only take the first 51 if there are more
    if current_count > 51:
        fixed_variations = fixed_variations[:51]
    
    # Write back the fixed data
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_variations, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def main():
    # Find all Grade 6 variation files
    variation_files = glob.glob('Gr6_*_variations.json')
    
    print(f"Found {len(variation_files)} Grade 6 variation files to process")
    
    success_count = 0
    failed_files = []
    
    for file_path in variation_files:
        print(f"Processing {file_path}...")
        if fix_variation_file(file_path):
            success_count += 1
        else:
            failed_files.append(file_path)
    
    print(f"\n{'='*50}")
    print(f"Successfully processed {success_count}/{len(variation_files)} files")
    
    if failed_files:
        print(f"\nFailed to process {len(failed_files)} files:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()