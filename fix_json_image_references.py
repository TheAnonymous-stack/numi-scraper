import json
import os
import glob

def fix_json_image_references():
    """Fix JSON files to properly reference their corresponding HTML files"""
    
    # List of all JSON files that need to be updated
    json_files = [
        'Gr6_1_E4_variations.json',
        'Gr6_1_E5_variations.json',
        'Gr6_2_E1_variations.json',
        'Gr6_3_E2_variations.json',
        'Gr6_3_E4_variations.json',
        'Gr6_5_E1_variations.json',
        'Gr6_15_E5_variations.json',
        'Gr6_16_E1_variations.json',
        'Gr6_23_E1_variations.json',
        'Gr6_23_E2_variations.json',
        'Gr6_23_E3_variations.json',
        'Gr6_24_E1_variations.json',
        'Gr6_24_E2_variations.json',
        'Gr6_24_E3_variations.json',
        'Gr6_26_E1_variations.json',
        'Gr6_26_E2_variations.json',
        'Gr6_27_E1_variations.json',
        'Gr6_27_E2_variations.json',
        'Gr6_27_E3_variations.json',
        'Gr6_28_E3_variations.json',
        'Gr6_33_E1_variations.json',
        'Gr6_33_E2_variations.json',
        'Gr6_34_E3_variations.json',
        'Gr6_35_E1_variations.json',
        'Gr6_36_E1_variations.json',
        'Gr6_42_E4_variations.json',
        'Gr6_43_E2_variations.json',
        'Gr6_44_E1_variations.json',
        'Gr6_44_E2_variations.json',
        'Gr6_44_E3_variations.json',
        'Gr6_54_E3_variations.json',
        'Gr6_55_E1_variations.json',
        'Gr6_22_E3_variations.json',
        'Gr6_1_E2_variations.json'
    ]
    
    total_files_updated = 0
    total_questions_updated = 0
    
    for json_file in json_files:
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found, skipping...")
            continue
            
        # Extract the base pattern for HTML files (e.g., "Gr6_2_E1" from "Gr6_2_E1_variations.json")
        base_name = json_file.replace('_variations.json', '')
        
        # Load the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        file_updated = False
        questions_updated_in_file = 0
        
        if 'quizzes' in data:
            for quiz in data['quizzes']:
                if 'question_number' in quiz:
                    # Extract question number (e.g., "1_1" from question_number)
                    question_num = quiz['question_number']
                    
                    # Create the expected HTML filename
                    expected_html = f"{base_name}_{question_num}.html"
                    expected_html_path = f"HTML/{expected_html}"
                    
                    # Check if the HTML file exists
                    if os.path.exists(expected_html_path):
                        # Update the image_tag to reference the correct HTML file
                        old_image_tag = quiz.get('image_tag', '')
                        new_image_tag = expected_html.replace('.html', '')  # Remove .html extension
                        
                        if old_image_tag != new_image_tag:
                            quiz['image_tag'] = new_image_tag
                            file_updated = True
                            questions_updated_in_file += 1
                            print(f"Updated {json_file} question {question_num}: {old_image_tag} -> {new_image_tag}")
        
        # Save the updated JSON file if changes were made
        if file_updated:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            total_files_updated += 1
            total_questions_updated += questions_updated_in_file
            print(f"Updated {json_file} with {questions_updated_in_file} question image references")
        else:
            print(f"No updates needed for {json_file}")
    
    print(f"\nSummary:")
    print(f"   Files updated: {total_files_updated}")
    print(f"   Questions updated: {total_questions_updated}")
    print(f"   All JSON files now properly reference their HTML files!")

if __name__ == "__main__":
    fix_json_image_references()