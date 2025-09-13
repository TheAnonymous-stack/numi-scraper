import json
import os
import re

def extract_table_data(backend_description):
    """Extract table data from backend description"""
    # Parse patterns like "The first column contains the numbers ... The second column contains the numbers ..."
    first_col_match = re.search(r'first column contains the numbers ([^.]+)', backend_description)
    second_col_match = re.search(r'second column contains the numbers ([^.]+)', backend_description)
    
    if not first_col_match or not second_col_match:
        return None, None
    
    # Extract column values
    first_col_text = first_col_match.group(1).strip()
    second_col_text = second_col_match.group(1).strip()
    
    # Parse values (replace "a blank box" with empty string)
    first_col_values = []
    for val in first_col_text.split(','):
        val = val.strip().rstrip('.')
        if 'blank' in val:
            first_col_values.append('')
        else:
            first_col_values.append(val)
    
    # Parse second column (should be "1, 2, 3, 4, and 5" or similar)
    second_col_values = []
    second_col_text = second_col_text.replace('and', ',').replace('.', '')
    for val in second_col_text.split(','):
        val = val.strip()
        if val:
            second_col_values.append(val)
    
    return first_col_values, second_col_values

def create_ratio_table_html(first_col, second_col, answer, question_num):
    """Create HTML with ratio table visualization"""
    
    # Find blank position and fill with answer for display
    blank_index = -1
    for i, val in enumerate(first_col):
        if val == '':
            blank_index = i
            break
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Ratio Table</title>
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
            margin-bottom: 20px;
            font-weight: bold;
            color: #333;
        }}
        .ratio-table {{
            margin: 20px auto;
            border-collapse: collapse;
            font-size: 18px;
        }}
        .ratio-table td {{
            border: 2px solid #333;
            padding: 15px 30px;
            text-align: center;
            min-width: 60px;
        }}
        .ratio-table tr:first-child td {{
            background-color: #e3f2fd;
            font-weight: bold;
        }}
        .blank-cell {{
            background-color: #fff3e0;
            position: relative;
        }}
        .answer {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .blank-indicator {{
            display: inline-block;
            width: 40px;
            height: 25px;
            border: 2px solid #666;
            background-color: #f9f9f9;
            vertical-align: middle;
        }}
        .info-text {{
            font-size: 14px;
            color: #666;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">Complete the ratio table.</div>
        
        <table class="ratio-table">
            <tr>
                <td>Column A</td>
                <td>Column B</td>
            </tr>"""
    
    # Add table rows
    for i in range(len(first_col)):
        html += "\n            <tr>"
        
        # First column cell
        if i == blank_index:
            html += f'\n                <td class="blank-cell"><span class="blank-indicator"></span></td>'
        else:
            html += f'\n                <td>{first_col[i]}</td>'
        
        # Second column cell
        html += f'\n                <td>{second_col[i]}</td>'
        html += "\n            </tr>"
    
    html += f"""
        </table>
        
        <div class="info-text">
            Find the missing value in the ratio table.
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_28_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        correct_answer = quiz['correct_answers'][0] if quiz.get('correct_answers') else ''
        
        # Extract table data
        first_col, second_col = extract_table_data(backend_desc)
        
        if first_col and second_col:
            # Create HTML content
            html_content = create_ratio_table_html(first_col, second_col, correct_answer, question_num)
            
            # Save HTML file
            filename = f'HTML/Gr6_28_E3_{question_num}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_count += 1
            print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()