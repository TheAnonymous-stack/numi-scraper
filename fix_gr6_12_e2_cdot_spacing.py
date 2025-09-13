import json
import re

def fix_cdot_spacing(text):
    """Fix the cdot spacing in the question text"""
    
    # Fix the pattern to ensure proper spacing around \cdot
    # Replace \_ with proper underscore formatting
    text = text.replace('\\cdot \\\_', '\\cdot \\_')
    text = text.replace('\\_', '\\underline{\\hspace{1cm}}')
    
    return text

def process_file():
    """Process and fix Gr6_12_E2_variations.json"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            
            # Fix the cdot spacing
            fixed = fix_cdot_spacing(original)
            
            if fixed != original:
                quiz['question_text'] = fixed
                fixed_count += 1
                print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E2_variations.json")

if __name__ == "__main__":
    process_file()