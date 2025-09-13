import json
import os
import re

def extract_table_data(backend_description):
    """Extract table data from backend description"""
    # Extract coordinate points from the description
    points_match = re.findall(r'\((\d+),\s*(\d+|\\?\[?blank\\?\]?)\)', backend_description)
    
    # Extract the table data if it exists
    table_match = re.search(r'table with two columns labeled x and y, showing values for ([^.]+)', backend_description)
    
    if table_match:
        table_text = table_match.group(1)
        # Parse table values
        table_values = []
        pairs = re.findall(r'\((\d+),\s*(\d+|\\?\[?blank\\?\]?)\)', table_text)
        for x, y in pairs:
            if 'blank' in y.lower():
                table_values.append((x, ''))
            else:
                table_values.append((x, y))
        return table_values
    
    return []

def create_graph_equation_html(table_data, question_num):
    """Create HTML with graph visualization and table"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Graph and Equation</title>
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
        .graph-container {{
            margin: 25px auto;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
        }}
        .graph-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        }}
        .table-container {{
            margin: 25px auto;
            display: inline-block;
        }}
        .data-table {{
            border-collapse: collapse;
            font-size: 16px;
        }}
        .data-table th {{
            border: 2px solid #333;
            padding: 10px 25px;
            background-color: #e3f2fd;
            font-weight: bold;
        }}
        .data-table td {{
            border: 2px solid #333;
            padding: 10px 25px;
            text-align: center;
        }}
        .blank-cell {{
            background-color: #fff3e0;
            min-width: 50px;
        }}
        .blank-indicator {{
            display: inline-block;
            width: 40px;
            height: 25px;
            border: 2px solid #666;
            background-color: #f9f9f9;
            vertical-align: middle;
        }}
        .input-section {{
            margin-top: 25px;
        }}
        .input-label {{
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }}
        .equation-input {{
            display: inline-block;
            margin: 10px;
        }}
        .equation-input label {{
            margin-right: 10px;
            font-size: 16px;
        }}
        .equation-input input {{
            width: 100px;
            padding: 5px;
            border: 2px solid #666;
            border-radius: 3px;
            font-size: 16px;
        }}
        .instructions {{
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
            Complete the table and write the equation for the relationship shown in the graph.<br>
            Write the equation without spaces (for example, x+1).
        </div>
        
        <div class="graph-container">
            <div class="graph-title">Coordinate Graph</div>
            <svg width="400" height="400" viewBox="0 0 400 400">
                <!-- Grid -->
                <defs>
                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="0.5"/>
                    </pattern>
                </defs>
                <rect width="400" height="400" fill="url(#grid)" />
                
                <!-- Axes -->
                <line x1="40" y1="360" x2="380" y2="360" stroke="#333" stroke-width="2"/>
                <line x1="40" y1="20" x2="40" y2="360" stroke="#333" stroke-width="2"/>
                
                <!-- Axis labels -->
                <text x="200" y="395" text-anchor="middle" font-size="14" fill="#333">x</text>
                <text x="15" y="200" text-anchor="middle" font-size="14" fill="#333" transform="rotate(-90 15 200)">y</text>
                
                <!-- Axis numbers -->
                <text x="40" y="375" text-anchor="middle" font-size="12" fill="#666">0</text>
                <text x="130" y="375" text-anchor="middle" font-size="12" fill="#666">5</text>
                <text x="220" y="375" text-anchor="middle" font-size="12" fill="#666">10</text>
                <text x="310" y="375" text-anchor="middle" font-size="12" fill="#666">15</text>
                
                <text x="25" y="365" text-anchor="middle" font-size="12" fill="#666">0</text>
                <text x="25" y="275" text-anchor="middle" font-size="12" fill="#666">5</text>
                <text x="25" y="185" text-anchor="middle" font-size="12" fill="#666">10</text>
                <text x="25" y="95" text-anchor="middle" font-size="12" fill="#666">15</text>
                
                <!-- Line (example - would be based on actual data) -->
                <line x1="40" y1="300" x2="340" y2="60" stroke="#4CAF50" stroke-width="2" stroke-dasharray="5,5"/>
                
                <!-- Arrow indicators -->
                <polygon points="335,55 345,60 335,65" fill="#4CAF50"/>
                <polygon points="45,305 35,300 45,295" fill="#4CAF50"/>
                
                <!-- Note -->
                <text x="200" y="40" text-anchor="middle" font-size="12" fill="#666">
                    (Graph shows a linear relationship)
                </text>
            </svg>
        </div>
        
        <div class="table-container">
            <table class="data-table">
                <tr>
                    <th>x</th>
                    <th>y</th>
                </tr>"""
    
    # Add table rows
    for x, y in table_data:
        if y == '':
            html += f"""
                <tr>
                    <td>{x}</td>
                    <td class="blank-cell"><span class="blank-indicator"></span></td>
                </tr>"""
        else:
            html += f"""
                <tr>
                    <td>{x}</td>
                    <td>{y}</td>
                </tr>"""
    
    html += """
            </table>
        </div>
        
        <div class="input-section">
            <div class="input-label">Fill in the missing value and write the equation:</div>
            <div class="equation-input">
                <label>Missing y-value:</label>
                <input type="text" placeholder="?">
            </div>
            <div class="equation-input">
                <label>Equation: y =</label>
                <input type="text" placeholder="x+?">
            </div>
        </div>
        
        <div class="instructions">
            1. Use the graph to find the missing y-value in the table<br>
            2. Look for the pattern between x and y values<br>
            3. Write the equation in the form y = x + constant
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_34_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        
        # Extract table data
        table_data = extract_table_data(backend_desc)
        
        # If no table data found, create default
        if not table_data:
            table_data = [('4', '18'), ('9', '23'), ('11', '25'), ('12', '')]
        
        # Create HTML content
        html_content = create_graph_equation_html(table_data, question_num)
        
        # Save HTML file
        filename = f'HTML/Gr6_34_E3_{question_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_count += 1
        print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()