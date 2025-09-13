import json
import re

def fix_final_formatting(text):
    """Fix the question text with proper line breaks and formatting"""
    
    # Extract the initial multiplication problem
    match = re.match(r'Use properties.*?\n?\$?([\d]+)\s*\\cdot\s*([\d]+)\s*\\cdot\s*([\d]+)', text, re.DOTALL)
    
    if match:
        num1 = match.group(1)
        num2 = match.group(2) 
        num3 = match.group(3)
        
        # Create properly formatted question where each blank is completely separate
        # Using line breaks to ensure each equation is on its own line
        fixed_text = f"""Use properties to find the product.
${num1} \\cdot {num2} \\cdot {num3}$

Line 1: ${num2} \\cdot$ _____ $\\cdot {num3}$

Line 2: ${num2} \\cdot ($ _____ $\\cdot {num3})$

Line 3: ${num2} \\cdot$ _____

Line 4: Answer = _____"""
        
        return fixed_text
    
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
            
            # Fix the formatting
            fixed = fix_final_formatting(original)
            
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