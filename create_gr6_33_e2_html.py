import json
import os
import re

def extract_pattern_data(backend_description):
    """Extract pattern rules and values from backend description"""
    # Parse pattern A
    pattern_a_match = re.search(r'Pattern A has the note (add \d+) written in italic, followed by the numbers ([^.]+)', backend_description)
    # Parse pattern B
    pattern_b_match = re.search(r'Pattern B has the note (add \d+) written in italic, followed by the numbers ([^.]+)', backend_description)
    
    if not pattern_a_match or not pattern_b_match:
        return None, None, None, None
    
    # Extract rules
    rule_a = pattern_a_match.group(1)
    rule_b = pattern_b_match.group(1)
    
    # Extract values for Pattern A
    values_a_text = pattern_a_match.group(2).strip()
    values_a = []
    for val in values_a_text.replace('and', ',').split(','):
        val = val.strip().rstrip('.')
        if val and val[0].isdigit() or (val[0] == '-' if len(val) > 1 else False):
            values_a.append(val)
    
    # Extract values for Pattern B
    values_b_text = pattern_b_match.group(2).strip()
    values_b = []
    for val in values_b_text.replace('and', ',').split(','):
        val = val.strip().rstrip('.')
        if val and val[0].isdigit() or (val[0] == '-' if len(val) > 1 else False):
            values_b.append(val)
    
    return rule_a, values_a, rule_b, values_b

def create_pattern_comparison_html(rule_a, values_a, rule_b, values_b, choices, question_num):
    """Create HTML with pattern comparison visualization"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Compare Number Patterns</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 700px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            font-weight: bold;
            color: #333;
        }}
        .patterns-table {{
            margin: 25px auto;
            border-collapse: collapse;
            font-size: 16px;
            width: 100%;
        }}
        .patterns-table th {{
            border: 2px solid #333;
            padding: 10px 15px;
            text-align: left;
            background-color: #e3f2fd;
            font-weight: bold;
            width: 20%;
        }}
        .patterns-table td {{
            border: 2px solid #333;
            padding: 10px 15px;
            text-align: center;
        }}
        .rule {{
            font-style: italic;
            color: #666;
            font-size: 14px;
            margin-left: 5px;
        }}
        .choices {{
            margin: 25px auto;
            text-align: left;
            max-width: 600px;
        }}
        .choice {{
            margin: 15px 0;
            padding: 12px 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
            text-align: left;
            line-height: 1.5;
        }}
        .choice:hover {{
            background-color: #e3f2fd;
        }}
        .choice-label {{
            font-weight: bold;
            margin-right: 10px;
        }}
        .explanation {{
            font-size: 14px;
            color: #666;
            margin-top: 20px;
            line-height: 1.5;
            text-align: left;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">Compare pattern A to pattern B. Which statement is true?</div>
        
        <table class="patterns-table">
            <tr>
                <th>Pattern A <span class="rule">({rule_a})</span></th>"""
    
    # Add Pattern A values
    for val in values_a:
        html += f"""
                <td>{val}</td>"""
    
    html += f"""
            </tr>
            <tr>
                <th>Pattern B <span class="rule">({rule_b})</span></th>"""
    
    # Add Pattern B values
    for val in values_b:
        html += f"""
                <td>{val}</td>"""
    
    html += """
            </tr>
        </table>
        
        <div class="choices">"""
    
    # Add choice options
    for i, choice in enumerate(choices):
        choice_label = "A" if i == 0 else "B"
        html += f"""
            <div class="choice">
                <span class="choice-label">{choice_label})</span>
                {choice}
            </div>"""
    
    html += """
        </div>
        
        <div class="explanation">
            To find the relationship between patterns, compare corresponding terms. 
            Check if Pattern B terms can be obtained by applying a consistent rule 
            to Pattern A terms (like multiplying and adding, or just adding a constant).
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_33_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        choices = quiz.get('choices', [])
        
        # Extract pattern data
        rule_a, values_a, rule_b, values_b = extract_pattern_data(backend_desc)
        
        if rule_a and values_a and rule_b and values_b:
            # Create HTML content
            html_content = create_pattern_comparison_html(
                rule_a, values_a, rule_b, values_b, choices, question_num
            )
            
            # Save HTML file
            filename = f'HTML/Gr6_33_E2_{question_num}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_count += 1
            print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()