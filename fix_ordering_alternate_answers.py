import json
import os

def remove_alternate_answers_from_ordering(file_path):
    """Remove has_alternate_answers flag from ordering questions"""
    
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        removed_count = 0
        
        # Check if it has quizzes array
        if 'quizzes' in data:
            for quiz in data['quizzes']:
                # Check if it's an ordering question with has_alternate_answers
                if quiz.get('question_type') == 'Ordering Items':
                    if 'has_alternate_answers' in quiz:
                        del quiz['has_alternate_answers']
                        modified = True
                        removed_count += 1
        
        # Save the file if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[FIXED] {file_path} - Removed has_alternate_answers from {removed_count} ordering questions")
            return True
        else:
            print(f"  No changes needed for {file_path}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix ordering questions with has_alternate_answers issue"""
    
    # List of files that may have this issue
    files_to_check = [
        'Gr6_2_E3_variations.json',
        'Gr6_4_E1_variations.json',
        'Gr6_4_E2_variations.json',
        'Gr6_4_E3_variations.json'
    ]
    
    print("Removing 'has_alternate_answers' from ordering questions...\n")
    
    fixed_count = 0
    for file_name in files_to_check:
        file_path = os.path.join(r'C:\Users\kapil\numi-scraper', file_name)
        if os.path.exists(file_path):
            print(f"Processing {file_name}...")
            if remove_alternate_answers_from_ordering(file_path):
                fixed_count += 1
        else:
            print(f"[NOT FOUND] File not found: {file_path}")
    
    print(f"\n{'='*60}")
    print(f"Summary: Fixed {fixed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()