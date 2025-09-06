import json
import os
import re
from glob import glob

def fix_all_json_files():
    """
    1. Remove regex underscores (\\_\\) and make them normal underscores
    2. Add =_ to EVERY single question_text 
    """
    
    files_processed = 0
    total_questions_fixed = 0
    
    # Find all Gr6 JSON files
    json_files = glob("Gr6_*_variations.json")
    
    for filename in json_files:
        try:
            print(f"Processing {filename}...")
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions_fixed_in_file = 0
            
            # Process each question in the file
            for question in data:
                if 'question_text' in question:
                    original_text = question['question_text']
                    
                    # Step 1: Fix regex underscores - replace \\_\\_ with normal underscores
                    fixed_text = original_text.replace('\\_\\_', '__')
                    fixed_text = fixed_text.replace('\\_', '_')
                    
                    # Step 2: Add =_ to every question if not already present
                    if not fixed_text.strip().endswith('=_'):
                        # Remove existing =_ if it exists somewhere in middle
                        fixed_text = fixed_text.replace('=_', '')
                        # Add =_ at the end
                        fixed_text = fixed_text.strip() + '=_'
                    
                    # Update the question
                    if fixed_text != original_text:
                        question['question_text'] = fixed_text
                        questions_fixed_in_file += 1
                
                # Also fix underscores in other text fields
                for field in ['answer', 'choices', 'solution']:
                    if field in question:
                        if isinstance(question[field], str):
                            question[field] = question[field].replace('\\_\\_', '__').replace('\\_', '_')
                        elif isinstance(question[field], list):
                            for i, choice in enumerate(question[field]):
                                if isinstance(choice, str):
                                    question[field][i] = choice.replace('\\_\\_', '__').replace('\\_', '_')
            
            # Save the file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            files_processed += 1
            total_questions_fixed += questions_fixed_in_file
            print(f"  Fixed {questions_fixed_in_file} questions")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\nSUMMARY:")
    print(f"Files processed: {files_processed}")
    print(f"Total questions fixed: {total_questions_fixed}")

if __name__ == "__main__":
    fix_all_json_files()