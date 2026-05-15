import json
import os
import re

def create_decimal_grid_html(shaded_count, question_num):
    """Create HTML for decimal grid visualization"""
    
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
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="visual-element">
            <div class="grid-label">The large square represents 1 whole</div>
            <svg height="400" viewBox="0 0 400 400" width="400">
                <!-- Outer border for the whole grid -->
                <rect x="50" y="50" width="300" height="300" fill="white" stroke="#000" stroke-width="2"></rect>
                
                <!-- Grid lines -->
                <g stroke="#ccc" stroke-width="0.5">
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
                <g fill="#4CAF50" fill-opacity="0.6">
"""
    
    # Shade the appropriate number of squares
    for i in range(shaded_count):
        row = i // 10
        col = i % 10
        x_pos = 50 + col * 30
        y_pos = 50 + row * 30
        html += f'                    <rect x="{x_pos}" y="{y_pos}" width="30" height="30" stroke="#4CAF50" stroke-width="1"></rect>\n'
    
    html += f"""                </g>
                
                <!-- Text label showing shaded count -->
                <text x="200" y="380" text-anchor="middle" font-family="Arial" font-size="14" fill="#333">
                    {shaded_count} out of 100 squares shaded
                </text>
            </svg>
        </div>
    </div>
</body>
</html>"""
    
    return html

def fix_gr6_5_e1_html():
    """Fix HTML files for Gr6_5_E1 to show proper decimal grids"""
    
    # Load the JSON file
    with open('Gr6_5_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    files_created = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        
        # Extract number of shaded squares from backend description
        # Pattern: "Out of the 100 squares, X squares are shaded"
        match = re.search(r'Out of the 100 squares, (\d+) squares? are shaded', backend_desc)
        if match:
            shaded_count = int(match.group(1))
        else:
            # Try alternate pattern: "X of the 100 small squares are shaded"
            match = re.search(r'(\d+) of the 100 small squares are shaded', backend_desc)
            if match:
                shaded_count = int(match.group(1))
            else:
                # Default to 1 if not found
                shaded_count = 1
        
        # Create the HTML
        html_content = create_decimal_grid_html(shaded_count, question_num)
        
        # Save the HTML file
        html_filename = f"HTML/Gr6_5_E1_{question_num}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        files_created += 1
        print(f"Created {html_filename} with {shaded_count} squares shaded")
    
    print(f"\nTotal files created: {files_created}")

if __name__ == "__main__":
    fix_gr6_5_e1_html()