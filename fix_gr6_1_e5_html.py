import json
import os
import re

def create_number_line_html(min_val, max_val, num1, num2, question_num):
    """Create HTML for number line comparison"""
    
    # Calculate appropriate spacing
    range_val = max_val - min_val
    width = 600 if range_val <= 10 else 800
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Compare Numbers</title>
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
            max-width: 1000px;
        }}
        .visual-element {{
            margin: 20px auto;
            display: inline-block;
            padding: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="visual-element">
            <svg height="150" viewBox="0 0 {width} 150" width="{width}">
                <!-- Number line -->
                <line stroke="#000" stroke-width="2" x1="50" x2="{width-50}" y1="75" y2="75"></line>
                
                <!-- Tick marks and labels -->
                <g stroke="#000" stroke-width="1" fill="#000" font-family="Arial" font-size="12" text-anchor="middle">
"""
    
    # Add tick marks for each integer
    tick_spacing = (width - 100) / (range_val)
    for i in range(int(range_val) + 1):
        val = min_val + i
        x_pos = 50 + i * tick_spacing
        html += f'                    <line x1="{x_pos}" x2="{x_pos}" y1="70" y2="80"></line>\n'
        # Label every number or every other number depending on range
        if range_val <= 20 or val % 2 == 0 or val % 5 == 0:
            html += f'                    <text x="{x_pos}" y="95">{val}</text>\n'
    
    # Highlight the two numbers being compared
    if min_val <= num1 <= max_val:
        x1 = 50 + ((num1 - min_val) / range_val) * (width - 100)
        html += f'                    <circle cx="{x1}" cy="75" r="8" fill="#4CAF50" stroke="#000" stroke-width="2"></circle>\n'
        html += f'                    <text x="{x1}" y="55" font-size="14" font-weight="bold" fill="#4CAF50">{num1}</text>\n'
    
    if min_val <= num2 <= max_val:
        x2 = 50 + ((num2 - min_val) / range_val) * (width - 100)
        html += f'                    <circle cx="{x2}" cy="75" r="8" fill="#2196F3" stroke="#000" stroke-width="2"></circle>\n'
        html += f'                    <text x="{x2}" y="120" font-size="14" font-weight="bold" fill="#2196F3">{num2}</text>\n'
    
    html += """                </g>
            </svg>
        </div>
    </div>
</body>
</html>"""
    
    return html

def fix_gr6_1_e5_html():
    """Fix HTML files for Gr6_1_E5 to show proper number lines"""
    
    # Load the JSON file
    with open('Gr6_1_E5_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    files_created = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        question_text = quiz['question_text']
        backend_desc = quiz.get('backend_description', '')
        
        # Extract the two numbers being compared from question text
        # Pattern: "Compare the numbers. Pick the correct sign. NUM1 NUM2"
        match = re.search(r'Pick the correct sign\.\s*(-?\d+)\s+(-?\d+)', question_text)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
        else:
            continue
        
        # Extract range from backend description
        # Pattern: "number line from MIN to MAX"
        range_match = re.search(r'number line from (-?\d+) to (-?\d+)', backend_desc)
        if range_match:
            min_val = int(range_match.group(1))
            max_val = int(range_match.group(2))
        else:
            # Default range based on the numbers
            min_val = min(num1, num2) - 2
            max_val = max(num1, num2) + 2
        
        # Create the HTML
        html_content = create_number_line_html(min_val, max_val, num1, num2, question_num)
        
        # Save the HTML file
        html_filename = f"HTML/Gr6_1_E5_{question_num}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        files_created += 1
        print(f"Created {html_filename} with number line from {min_val} to {max_val}, comparing {num1} and {num2}")
    
    print(f"\nTotal files created: {files_created}")

if __name__ == "__main__":
    fix_gr6_1_e5_html()