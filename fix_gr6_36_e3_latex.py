import json

def fix_latex_formatting(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            question_text = quiz['question_text']
            
            # Check if this is the problematic pattern with all equations in one $ block
            if question_text.startswith("Complete the pattern: $") and "\\div = _" in question_text:
                # Extract the base number (e.g., 0.8996)
                import re
                base_match = re.search(r'\$([0-9.]+)', question_text)
                if base_match:
                    base_num = base_match.group(1)
                    
                    # Extract all the result numbers
                    results = re.findall(r'= ([0-9.]+)', question_text)
                    
                    if len(results) >= 4:
                        # Rebuild the question with proper formatting
                        new_text = "Complete the pattern: "
                        new_text += f"${base_num} \\div$ _ $= {results[0]}$ "
                        new_text += f"${base_num} \\div$ _ $= {results[1]}$ "
                        new_text += f"${base_num} \\div$ _ $= {results[2]}$ "
                        new_text += f"${base_num} \\div$ _ $= {results[3]}$=_"
                        
                        quiz['question_text'] = new_text
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed LaTeX formatting in {filename}")

# Process the file
fix_latex_formatting('Gr6_36_E3_variations.json')