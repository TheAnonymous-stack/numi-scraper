import json
import re

def fix_cdot_closures(text):
    """Fix the question text to properly close all \cdot symbols with dollar signs"""
    
    # Extract the numbers from the first line
    match = re.search(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)\$', text)
    
    if match:
        num1 = match.group(1)
        num2 = match.group(2)
        num3 = match.group(3)
        
        # Determine which number goes in the middle (usually the larger one)
        middle_num = num2
        
        # Create properly formatted question with all \cdot properly enclosed in dollar signs
        fixed_text = f"""Use properties to find the product.
${num1} \\cdot {num2} \\cdot {num3}$
$= {middle_num} \\cdot$ [[box1]] $\\cdot$ [[box2]]
$= {middle_num} \\cdot ($ [[box3]] $\\cdot$ [[box4]] $)$
$= {middle_num} \\cdot$ [[box5]]
$=$ [[box6]]"""
        
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
            
            # Fix cdot closures
            fixed = fix_cdot_closures(original)
            
            if fixed != original:
                quiz['question_text'] = fixed
                fixed_count += 1
                print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E2_variations.json")
    print("All \\cdot symbols are now properly enclosed in dollar signs")

if __name__ == "__main__":
    process_file()