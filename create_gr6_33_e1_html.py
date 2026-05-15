import json
import os
import re

def extract_table_values(backend_description):
    """Extract x and y values from backend description"""
    # Parse patterns like "The first column contains the numbers ... The second column contains the numbers ..."
    first_col_match = re.search(r'first column contains the numbers ([^.]+)', backend_description)
    second_col_match = re.search(r'second column contains the numbers ([^.]+)', backend_description)
    
    if not first_col_match or not second_col_match:
        return None, None
    
    # Extract column values
    first_col_text = first_col_match.group(1).strip()
    second_col_text = second_col_match.group(1).strip()
    
    # Parse x values (first column)
    x_values = []
    for val in first_col_text.replace('and', ',').split(','):
        val = val.strip()
        if val:
            # Extract just the number, ignoring any semicolons or other text
            num_match = re.search(r'(-?\d+)', val)
            if num_match:
                x_values.append(num_match.group(1))
    
    # Parse y values (second column)
    y_values = []
    for val in second_col_text.replace('and', ',').replace('in the same order', '').split(','):
        val = val.strip()
        if val:
            # Extract just the number
            num_match = re.search(r'(-?\d+)', val)
            if num_match:
                y_values.append(num_match.group(1))
    
    return x_values, y_values

def create_function_table_html(x_values, y_values, answer, question_num):
    """Create HTML with function table visualization"""
    
    # Determine if answer is Linear (A) or Nonlinear (B)
    answer_text = "Linear" if answer == "A" else "Nonlinear"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Linear vs Nonlinear Functions</title>
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
            max-width: 600px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            font-weight: bold;
            color: #333;
        }}
        .function-table {{
            margin: 25px auto;
            border-collapse: collapse;
            font-size: 18px;
        }}
        .function-table th {{
            border: 2px solid #333;
            padding: 12px 30px;
            text-align: center;
            background-color: #e3f2fd;
            font-weight: bold;
        }}
        .function-table td {{
            border: 2px solid #333;
            padding: 12px 30px;
            text-align: center;
            min-width: 60px;
        }}
        .choices {{
            margin: 25px auto;
            text-align: left;
            display: inline-block;
        }}
        .choice {{
            margin: 10px 0;
            padding: 10px 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .choice:hover {{
            background-color: #e3f2fd;
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
        <div class="question">The table shows a function. Is the function linear or nonlinear?</div>
        
        <table class="function-table">
            <tr>
                <th>x</th>
                <th>y</th>
            </tr>"""
    
    # Add table rows
    for i in range(len(x_values)):
        html += f"""
            <tr>
                <td>{x_values[i]}</td>
                <td>{y_values[i]}</td>
            </tr>"""
    
    html += f"""
        </table>
        
        <div class="choices">
            <div class="choice">A) Linear</div>
            <div class="choice">B) Nonlinear</div>
        </div>
        
        <div class="explanation">
            To determine if a function is linear, check if the rate of change 
            (slope) between any two points is constant. If the rate of change 
            varies, the function is nonlinear.
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_33_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        correct_answer = quiz['correct_answers'][0] if quiz.get('correct_answers') else ''
        
        # Extract table values
        x_values, y_values = extract_table_values(backend_desc)
        
        if x_values and y_values:
            # Create HTML content
            html_content = create_function_table_html(x_values, y_values, correct_answer, question_num)
            
            # Save HTML file
            filename = f'HTML/Gr6_33_E1_{question_num}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_count += 1
            print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()