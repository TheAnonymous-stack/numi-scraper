import json
import os
import re

def create_gr6_54_e3_html(quiz):
    """Create HTML for balance a budget questions"""
    question_num = quiz['question_number']
    question_text = quiz.get('question_text', '')
    
    # Extract budget title from backend description
    title_match = re.search(r"'([^']+budget)'", quiz.get('backend_description', ''))
    budget_title = title_match.group(1) if title_match else "Monthly Budget"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Balance a Budget</title>
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
            font-size: 17px;
            margin-bottom: 20px;
            color: #333;
            line-height: 1.4;
        }}
        .budget-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #1976d2;
        }}
        .budget-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .budget-table th {{
            background-color: #e3f2fd;
            padding: 12px;
            border: 2px solid #333;
            font-weight: bold;
        }}
        .budget-table td {{
            padding: 10px;
            border: 1px solid #666;
            text-align: left;
        }}
        .total-row {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        .blank-input {{
            width: 80px;
            padding: 5px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 14px;
            text-align: center;
        }}
        .section-divider {{
            border-top: 2px solid #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">Complete the table to balance the budget.</div>
        
        <div class="budget-title">{budget_title}</div>
        
        <table class="budget-table">
            <tr>
                <th style="width: 50%;">Income</th>
                <th style="width: 50%;">Expenses</th>
            </tr>
            <tr>
                <td>Streaming: $175</td>
                <td>Equipment: $<input type="text" class="blank-input"></td>
            </tr>
            <tr>
                <td>Donations: $240</td>
                <td>Internet: $80</td>
            </tr>
            <tr>
                <td>Testing: $45</td>
                <td>Supplies: $30</td>
            </tr>
            <tr class="total-row section-divider">
                <td>Total: $<input type="text" class="blank-input"></td>
                <td>Total: $<input type="text" class="blank-input"></td>
            </tr>
        </table>
        
        <div style="font-size: 14px; color: #666; margin-top: 15px;">
            Balance the budget: Income = Expenses
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_54_E3_{question_num}.html"

def create_gr6_55_e1_html(quiz):
    """Create HTML for adjust a budget questions"""
    question_num = quiz['question_number']
    question_text = quiz.get('question_text', '')
    choices = quiz.get('choices', [])
    
    # Extract budget title from backend description
    title_match = re.search(r"'([^']+budget)'", quiz.get('backend_description', ''))
    budget_title = title_match.group(1) if title_match else "Monthly Budget"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Adjust a Budget</title>
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
            max-width: 650px;
        }}
        .question {{
            font-size: 17px;
            margin-bottom: 20px;
            color: #333;
            line-height: 1.4;
        }}
        .budget-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #1976d2;
        }}
        .budget-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .budget-table th {{
            background-color: #e3f2fd;
            padding: 12px;
            border: 2px solid #333;
            font-weight: bold;
        }}
        .budget-table td {{
            padding: 10px;
            border: 1px solid #666;
            text-align: left;
        }}
        .choices {{
            margin: 25px 0;
            text-align: left;
        }}
        .choice {{
            margin: 10px 0;
            padding: 12px 15px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .choice:hover {{
            background-color: #e3f2fd;
        }}
        .choice-label {{
            font-weight: bold;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">What could be done to balance the budget?</div>
        
        <div class="budget-title">{budget_title}</div>
        
        <table class="budget-table">
            <tr>
                <th style="width: 50%;">Income</th>
                <th style="width: 50%;">Expenses</th>
            </tr>
            <tr>
                <td>Job: $40</td>
                <td>Equipment: $45</td>
            </tr>
            <tr>
                <td>Prize: $35</td>
                <td>Games: $52</td>
            </tr>
            <tr>
                <td>Reviews: $72</td>
                <td>Subscription: $75</td>
            </tr>
        </table>
        
        <div class="choices">"""
    
    # Add choices
    for i, choice in enumerate(choices[:4]):
        choice_label = chr(65 + i)
        html += f"""
            <div class="choice">
                <span class="choice-label">{choice_label})</span> {choice}
            </div>"""
    
    html += """
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_55_E1_{question_num}.html"

def main():
    os.makedirs('HTML', exist_ok=True)
    
    # Process Gr6_54_E3
    print("Processing Gr6_54_E3_variations.json...")
    with open('Gr6_54_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for quiz in data['quizzes']:
        html_content, filename = create_gr6_54_e3_html(quiz)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        count += 1
        print(f"Created {filename}")
    
    print(f"Created {count} files for Gr6_54_E3\n")
    
    # Process Gr6_55_E1
    print("Processing Gr6_55_E1_variations.json...")
    with open('Gr6_55_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for quiz in data['quizzes']:
        html_content, filename = create_gr6_55_e1_html(quiz)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        count += 1
        print(f"Created {filename}")
    
    print(f"Created {count} files for Gr6_55_E1")

if __name__ == "__main__":
    main()