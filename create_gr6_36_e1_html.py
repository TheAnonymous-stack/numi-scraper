import json
import os
import re

def extract_table_data(backend_description):
    """Extract input/output table data from backend description"""
    # Parse input values
    input_match = re.search(r"Input \(c\)'[^']*contains the numbers ([^.]+)", backend_description)
    # Parse output values
    output_match = re.search(r"Output \(d\)'[^']*contains the numbers ([^.]+)", backend_description)
    
    if not input_match or not output_match:
        return None, None
    
    # Extract input values
    input_text = input_match.group(1).strip()
    input_values = []
    for val in input_text.replace('and', ',').split(','):
        val = val.strip().rstrip('.')
        if val and (val[0].isdigit() or val[0] == '-'):
            input_values.append(val)
    
    # Extract output values
    output_text = output_match.group(1).strip()
    output_values = []
    for val in output_text.replace('and', ',').replace('in the same order', '').split(','):
        val = val.strip().rstrip('.')
        if val and (val[0].isdigit() or val[0] == '-'):
            output_values.append(val)
    
    return input_values, output_values

def extract_rule(question_text):
    """Extract the rule from question text"""
    rule_match = re.search(r'Rule: (.+?)\.', question_text)
    if rule_match:
        return rule_match.group(1)
    return "The output follows a specific rule"

def extract_pattern_data(question_text):
    """Extract pattern data for non-table questions"""
    # Look for pattern numbers
    pattern_match = re.search(r'pattern is (.+?)\..*The rule', question_text)
    if pattern_match:
        pattern_text = pattern_match.group(1)
        numbers = re.findall(r'\d+', pattern_text)
        return numbers
    return None

def create_table_check_html(input_values, output_values, rule, choices, question_text, question_num):
    """Create HTML for table checking questions"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Check Input/Output Table</title>
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
            margin-bottom: 20px;
            font-weight: bold;
            color: #333;
            line-height: 1.5;
        }}
        .rule-box {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 16px;
        }}
        .rule-label {{
            font-weight: bold;
            color: #1976d2;
        }}
        .table-container {{
            margin: 25px auto;
            display: inline-block;
        }}
        .io-table {{
            border-collapse: collapse;
            font-size: 16px;
        }}
        .io-table th {{
            border: 2px solid #333;
            padding: 12px 20px;
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        .io-table td {{
            border: 2px solid #333;
            padding: 12px 20px;
            text-align: center;
            min-width: 50px;
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
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">
            Gordon tried to complete this input/output table using the rule.<br>
            Is Gordon's table correct?
        </div>
        
        <div class="rule-box">
            <span class="rule-label">Rule:</span> {rule}
        </div>
        
        <div class="table-container">
            <table class="io-table">
                <tr>
                    <th>Input (c)</th>"""
    
    # Add input values as headers
    for val in input_values:
        html += f"""
                    <td>{val}</td>"""
    
    html += """
                </tr>
                <tr>
                    <th>Output (d)</th>"""
    
    # Add output values
    for val in output_values:
        html += f"""
                    <td>{val}</td>"""
    
    html += """
                </tr>
            </table>
        </div>
        
        <div class="choices">"""
    
    # Add choice options
    for i, choice in enumerate(choices):
        choice_label = chr(65 + i)  # A, B, C
        html += f"""
            <div class="choice">
                <span class="choice-label">{choice_label})</span>
                {choice}
            </div>"""
    
    html += """
        </div>
        
        <div class="explanation">
            Check if each output value follows the given rule when applied to its input value.
        </div>
    </div>
</body>
</html>"""
    
    return html

def create_pattern_check_html(pattern_numbers, rule, choices, question_text, question_num):
    """Create HTML for pattern checking questions"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Check Number Pattern</title>
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
            line-height: 1.5;
        }}
        .pattern-box {{
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border: 2px solid #ddd;
        }}
        .pattern-numbers {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            letter-spacing: 2px;
        }}
        .rule-box {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 16px;
        }}
        .rule-label {{
            font-weight: bold;
            color: #1976d2;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="question">
            {question_text.split('?')[0]}?
        </div>
        
        <div class="pattern-box">
            <div class="pattern-numbers">
                {', '.join(pattern_numbers) if pattern_numbers else '97, 83, 69, ...'}
            </div>
        </div>
        
        <div class="rule-box">
            <span class="rule-label">Rule:</span> {rule if rule else 'subtract 14'}
        </div>
        
        <div class="choices">"""
    
    # Add choice options
    for i, choice in enumerate(choices):
        choice_label = chr(65 + i)  # A, B, C
        html += f"""
            <div class="choice">
                <span class="choice-label">{choice_label})</span>
                {choice}
            </div>"""
    
    html += """
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_36_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        question_text = quiz.get('question_text', '')
        backend_desc = quiz.get('backend_description', '')
        choices = quiz.get('choices', [])
        
        # Extract the rule
        rule = extract_rule(question_text)
        
        if backend_desc and 'Input (c)' in backend_desc:
            # This is a table question
            input_values, output_values = extract_table_data(backend_desc)
            
            if input_values and output_values:
                html_content = create_table_check_html(
                    input_values, output_values, rule, choices, question_text, question_num
                )
            else:
                # Default values if parsing fails
                input_values = ['2', '5', '6', '11']
                output_values = ['7', '10', '11', '16']
                html_content = create_table_check_html(
                    input_values, output_values, rule, choices, question_text, question_num
                )
        else:
            # This is a pattern question
            pattern_numbers = extract_pattern_data(question_text)
            html_content = create_pattern_check_html(
                pattern_numbers, rule, choices, question_text, question_num
            )
        
        # Save HTML file
        filename = f'HTML/Gr6_36_E1_{question_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_count += 1
        print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()