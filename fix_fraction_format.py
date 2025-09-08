import json
import glob
import re

def needs_fraction_format(variation):
    """Check if this variation needs the _ _/_ format"""
    question_type = variation.get('question_type', '')
    question_text = variation.get('question_text', '')
    correct_answers = variation.get('correct_answers', [])
    
    # Check if it's a Multiple fill in the blank with 3 answers (whole, numerator, denominator)
    if question_type == 'Multiple fill in the blank' and len(correct_answers) == 3:
        # Check if it mentions mixed number or fraction in the text
        if ('mixed number' in question_text.lower() or 
            'fraction' in question_text.lower() or
            'whole or mixed number' in question_text.lower()):
            # Check if it doesn't already have the format
            if '_ _/_' not in question_text:
                return True
    
    return False

def fix_fraction_format_in_question(question_text):
    """Add _ _/_ format to question text if needed"""
    # Replace =_ with =_ _/_ if not already present
    if '=_' in question_text and '_ _/_' not in question_text:
        question_text = question_text.replace('=_', '=_ _/_')
    
    # Also handle cases where there might be spaces or formatting issues
    question_text = re.sub(r'=\s*_\s*$', '=_ _/_', question_text)
    
    return question_text

def fix_variation_file(file_path):
    """Fix fraction format in a single variation file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    modified = False
    
    for variation in data:
        # Check if this variation needs the fraction format
        if needs_fraction_format(variation):
            original_text = variation['question_text']
            fixed_text = fix_fraction_format_in_question(original_text)
            
            if original_text != fixed_text:
                variation['question_text'] = fixed_text
                modified = True
                print(f"  Fixed fraction format in {file_path}")
        
        # Also ensure orderMatter is True for fraction questions
        if (variation.get('question_type') == 'Multiple fill in the blank' and 
            len(variation.get('correct_answers', [])) == 3 and
            ('mixed number' in variation.get('question_text', '').lower() or '_ _/_' in variation.get('question_text', ''))):
            if not variation.get('orderMatter', False):
                variation['orderMatter'] = True
                modified = True
    
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    return False

def main():
    # Find all Grade 6 variation files
    variation_files = glob.glob('Gr6_*_variations.json')
    
    print(f"Checking {len(variation_files)} Grade 6 files for fraction format issues...")
    print()
    
    fixed_count = 0
    
    for file_path in variation_files:
        if fix_variation_file(file_path):
            fixed_count += 1
    
    print()
    print(f"Fixed fraction format in {fixed_count} files")

if __name__ == "__main__":
    main()