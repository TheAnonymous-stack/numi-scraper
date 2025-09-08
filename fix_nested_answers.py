import json
import glob
import os

def fix_correct_answers(correct_answers, question_type):
    """Fix the correct_answers format based on question type"""
    if not isinstance(correct_answers, list):
        return correct_answers
    
    # For Fill in the blank questions
    if question_type == "Fill in the blank":
        # Should be a simple list with one answer (or alternate answers)
        if len(correct_answers) == 1 and isinstance(correct_answers[0], list):
            # If there's only one nested list, check if it has multiple alternatives
            if len(correct_answers[0]) == 1:
                # Single answer, remove nesting
                return [correct_answers[0][0]]
            else:
                # Multiple alternatives, keep nested
                return correct_answers[0]
        return correct_answers
    
    # For Multiple fill in the blank questions  
    elif question_type in ["Multiple fill in the blank", "Multiple Fill in the blank"]:
        # Check if it's unnecessarily nested
        if correct_answers and isinstance(correct_answers[0], list):
            # Check if all elements are single-item lists (unnecessary nesting)
            all_single = all(isinstance(item, list) and len(item) == 1 for item in correct_answers)
            if all_single:
                # Flatten the unnecessary nesting
                return [item[0] if isinstance(item, list) else item for item in correct_answers]
            
            # Check if it's a single nested list that should be flattened
            if len(correct_answers) == 1 and isinstance(correct_answers[0], list):
                # This is likely the answer list wrapped in another list
                return correct_answers[0]
        
        return correct_answers
    
    return correct_answers

def fix_variation_file(file_path):
    """Fix all issues in a single variation file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    
    for variation in data:
        # Fix question_type capitalization
        if variation.get('question_type') == 'Multiple Fill in the blank':
            variation['question_type'] = 'Multiple fill in the blank'
            modified = True
        
        # Fix correct_answers format
        if 'correct_answers' in variation:
            original = variation['correct_answers']
            fixed = fix_correct_answers(original, variation.get('question_type', ''))
            if original != fixed:
                variation['correct_answers'] = fixed
                modified = True
        
        # Ensure orderMatter is set for Multiple fill in the blank with fractions
        if variation.get('question_type') == 'Multiple fill in the blank':
            # Check if it's a fraction question (has mixed number format in question_text)
            if 'question_text' in variation and ('_/_' in variation['question_text'] or 'mixed number' in variation['question_text']):
                if 'orderMatter' not in variation or variation['orderMatter'] != True:
                    variation['orderMatter'] = True
                    modified = True
            elif 'orderMatter' not in variation:
                variation['orderMatter'] = False
                modified = True
    
    if modified:
        # Write back the fixed data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    
    return False

def main():
    # Find all Grade 6 variation files
    variation_files = glob.glob('Gr6_*_variations.json')
    
    print(f"Found {len(variation_files)} Grade 6 variation files to process")
    
    fixed_count = 0
    for file_path in variation_files:
        if fix_variation_file(file_path):
            print(f"Fixed: {file_path}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files with nested answer issues")

if __name__ == "__main__":
    main()