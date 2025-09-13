import json
import os
import re

def create_decimal_grid_html(whole_value, shaded_count, correct_answer, question_num):
    """Create HTML for decimal grid visualization with proper mathematical representation"""
    
    # Calculate what the shaded squares should actually represent
    # If the square represents X whole, and we shade Y squares, it represents X * Y/100
    actual_decimal = whole_value * shaded_count / 100
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Decimal Grid</title>
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
        .visual-element {{
            margin: 20px auto;
            display: inline-block;
            padding: 10px;
        }}
        .grid-label {{
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
            font-weight: bold;
        }}
        .info-text {{
            font-size: 14px;
            margin-top: 10px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="visual-element">
            <div class="grid-label">The large square represents {whole_value} whole</div>
            <svg height="400" viewBox="0 0 400 400" width="400">
                <!-- Outer border for the whole grid -->
                <rect x="50" y="50" width="300" height="300" fill="white" stroke="#000" stroke-width="2"></rect>
                
                <!-- Grid lines -->
                <g stroke="#999" stroke-width="0.5">
"""
    
    # Add vertical grid lines
    for i in range(1, 10):
        x_pos = 50 + i * 30
        html += f'                    <line x1="{x_pos}" x2="{x_pos}" y1="50" y2="350"></line>\n'
    
    # Add horizontal grid lines
    for i in range(1, 10):
        y_pos = 50 + i * 30
        html += f'                    <line x1="50" x2="350" y1="{y_pos}" y2="{y_pos}"></line>\n'
    
    html += """                </g>
                
                <!-- Shaded squares -->
                <g fill="#4CAF50" fill-opacity="0.7">
"""
    
    # Shade the appropriate number of squares
    for i in range(shaded_count):
        row = i // 10
        col = i % 10
        x_pos = 50 + col * 30
        y_pos = 50 + row * 30
        html += f'                    <rect x="{x_pos}" y="{y_pos}" width="30" height="30" stroke="#4CAF50" stroke-width="1"></rect>\n'
    
    html += f"""                </g>
                
                <!-- Text labels -->
                <text x="200" y="380" text-anchor="middle" font-family="Arial" font-size="14" fill="#333">
                    {shaded_count} out of 100 squares shaded
                </text>
            </svg>
            <div class="info-text">
                Each small square = {whole_value}/100 = {whole_value/100:.2f}<br>
                {shaded_count} squares = {shaded_count} × {whole_value/100:.2f} = {actual_decimal:.2f}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html

def fix_gr6_5_e1_html():
    """Fix HTML files for Gr6_5_E1 to show proper decimal grids with correct mathematical relationships"""
    
    # Load the JSON file
    with open('Gr6_5_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    files_created = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        question_text = quiz.get('question_text', '')
        correct_answer = quiz.get('correct_answers', ['0.01'])[0]
        
        # Extract the whole value from question text
        # Pattern: "The large square represents X whole"
        match = re.search(r'The large square represents (\d+) whole', question_text)
        if match:
            whole_value = int(match.group(1))
        else:
            whole_value = 1
        
        # Since all answers are 0.01 in the current data, but this doesn't make mathematical sense,
        # let's calculate what should actually be shaded
        # If answer is 0.01 and square represents X whole, then we need 0.01/X * 100 squares shaded
        
        # For now, let's show 1 square shaded as per the data, but add explanatory text
        shaded_count = 1
        
        # However, if we wanted it to be mathematically correct:
        # To get 0.01 when square = whole_value, we'd need: 0.01 = whole_value * (shaded/100)
        # So shaded = 0.01 * 100 / whole_value = 1 / whole_value
        # But this would give fractional squares for whole_value > 1
        
        # Let's keep it simple and show what the data says, with proper labels
        
        # Create the HTML
        html_content = create_decimal_grid_html(whole_value, shaded_count, correct_answer, question_num)
        
        # Save the HTML file
        html_filename = f"HTML/Gr6_5_E1_{question_num}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        files_created += 1
        print(f"Created {html_filename} - Square represents {whole_value} whole, {shaded_count} squares shaded")
    
    print(f"\nTotal files created: {files_created}")
    print("\nNote: The JSON data appears to have incorrect mathematical relationships.")
    print("All questions show 1 square shaded with answer 0.01, regardless of what the square represents.")
    print("Mathematically, if square = X whole, then 1 shaded square = 0.01*X, not always 0.01")

if __name__ == "__main__":
    fix_gr6_5_e1_html()