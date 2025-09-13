import json
import re
import os

def fix_ordering_questions(file_path):
    """Fix ordering questions format by removing '=_' from question text"""
    
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        # Check if it has quizzes array
        if 'quizzes' in data:
            for quiz in data['quizzes']:
                # Check if it's an ordering question with the '=_' issue
                if quiz.get('question_type') == 'Ordering Items':
                    if 'question_text' in quiz:
                        # Remove '=_' from the end of question text
                        original_text = quiz['question_text']
                        cleaned_text = re.sub(r'\.?=_$', '.', original_text)
                        
                        # Also ensure proper punctuation
                        if not cleaned_text.endswith('.'):
                            cleaned_text += '.'
                        
                        if original_text != cleaned_text:
                            quiz['question_text'] = cleaned_text
                            modified = True
                            print(f"  Fixed: '{original_text}' -> '{cleaned_text}'")
        
        # Save the file if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[FIXED] {file_path}")
            return True
        else:
            print(f"  No changes needed for {file_path}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all problematic Grade 6 ordering questions"""
    
    # List of files to fix
    files_to_fix = [
        'Gr6_2_E3_variations.json',
        'Gr6_4_E1_variations.json', 
        'Gr6_4_E2_variations.json',
        'Gr6_4_E3_variations.json'
    ]
    
    print("Fixing ordering questions format...\n")
    
    fixed_count = 0
    for file_name in files_to_fix:
        file_path = os.path.join(r'C:\Users\kapil\numi-scraper', file_name)
        if os.path.exists(file_path):
            print(f"Processing {file_name}...")
            if fix_ordering_questions(file_path):
                fixed_count += 1
        else:
            print(f"[NOT FOUND] File not found: {file_path}")
    
    print(f"\n{'='*60}")
    print(f"Summary: Fixed {fixed_count} out of {len(files_to_fix)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()