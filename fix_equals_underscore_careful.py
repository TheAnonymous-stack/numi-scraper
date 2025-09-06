import json
import os
import re
from glob import glob

def fix_question_endings():
    """
    Carefully add =_ to question_text endings without creating duplicates or overlaps
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
                    original_text = question['question_text'].strip()
                    
                    # Remove any existing =_ patterns at the end first
                    cleaned_text = re.sub(r'=_+$', '', original_text)
                    cleaned_text = re.sub(r'=\s*_+\s*$', '', cleaned_text)
                    cleaned_text = re.sub(r'_+\s*=\s*_*$', '', cleaned_text)
                    cleaned_text = re.sub(r'=+_*=*\+*_*=*\+*$', '', cleaned_text)
                    
                    # Clean up any trailing spaces or punctuation
                    cleaned_text = cleaned_text.strip()
                    
                    # Add exactly one =_ at the end
                    final_text = cleaned_text + '=_'
                    
                    # Update the question if it changed
                    if final_text != original_text:
                        question['question_text'] = final_text
                        questions_fixed_in_file += 1
                        print(f"    Fixed: '{original_text}' -> '{final_text}'")
            
            # Save the file if any changes were made
            if questions_fixed_in_file > 0:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                files_processed += 1
                total_questions_fixed += questions_fixed_in_file
                print(f"  Updated {questions_fixed_in_file} questions in {filename}")
            else:
                print(f"  No changes needed in {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\nFINAL SUMMARY:")
    print(f"Files processed: {files_processed}")
    print(f"Total questions fixed: {total_questions_fixed}")

if __name__ == "__main__":
    fix_question_endings()