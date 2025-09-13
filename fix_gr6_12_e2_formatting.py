import json

def fix_formatting_issues(filename):
    """Fix formatting issues in the JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = 0
    
    for quiz in data['quizzes']:
        # Fix orderMatter field - convert string to boolean
        if 'orderMatter' in quiz:
            if isinstance(quiz['orderMatter'], str):
                if quiz['orderMatter'].upper() == "TRUE":
                    quiz['orderMatter'] = True
                    changes_made += 1
                elif quiz['orderMatter'].upper() == "FALSE":
                    quiz['orderMatter'] = False
                    changes_made += 1
        
        # Fix has_alternate_answers field - convert string to boolean if needed
        if 'has_alternate_answers' in quiz:
            if isinstance(quiz['has_alternate_answers'], str):
                if quiz['has_alternate_answers'].upper() == "TRUE":
                    quiz['has_alternate_answers'] = True
                    changes_made += 1
                elif quiz['has_alternate_answers'].upper() == "FALSE":
                    quiz['has_alternate_answers'] = False
                    changes_made += 1
    
    # Write the fixed data back to file with proper formatting
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed {changes_made} formatting issues in {filename}")
    return changes_made

# Process the file
changes = fix_formatting_issues('Gr6_12_E2_variations.json')
print(f"Total changes made: {changes}")
print("Done!")