import json
import os
import re

def create_gr6_42_e4_html(quiz):
    """Create HTML for frequency table from dot plot"""
    question_num = quiz['question_number']
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Frequency Table</title>
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
            color: #333;
        }}
        .dot-plot {{
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .plot-title {{
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .x-marks {{
            font-size: 20px;
            color: #ff6b35;
            letter-spacing: 2px;
        }}
        .table {{
            margin: 20px auto;
            border-collapse: collapse;
        }}
        .table th, .table td {{
            border: 2px solid #333;
            padding: 10px 20px;
            text-align: center;
        }}
        .table th {{
            background-color: #e3f2fd;
        }}
        .blank {{
            display: inline-block;
            width: 40px;
            height: 25px;
            border: 2px solid #666;
            background: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">Use the data in the line plot to complete the frequency chart below.</div>
        
        <div class="dot-plot">
            <div class="plot-title">Data Collection</div>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <div>0<br><span class="x-marks">XX</span></div>
                <div>1<br><span class="x-marks">XXXXX</span></div>
                <div>2<br><span class="x-marks">X</span></div>
                <div>3<br><span class="x-marks">XX</span></div>
                <div>4<br><span class="x-marks">XXXX</span></div>
            </div>
        </div>
        
        <table class="table">
            <tr>
                <th>Value</th>
                <th>Count</th>
            </tr>
            <tr><td>0</td><td>2</td></tr>
            <tr><td>1</td><td>5</td></tr>
            <tr><td>2</td><td>1</td></tr>
            <tr><td>3</td><td>2</td></tr>
            <tr><td>4</td><td><span class="blank"></span></td></tr>
        </table>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_42_E4_{question_num}.html"

def create_gr6_43_e2_html(quiz):
    """Create HTML for finding mode from table"""
    question_num = quiz['question_number']
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Find the Mode</title>
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
            max-width: 500px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            color: #333;
        }}
        .table {{
            margin: 20px auto;
            border-collapse: collapse;
        }}
        .table th, .table td {{
            border: 2px solid #333;
            padding: 10px 20px;
            text-align: center;
        }}
        .table th {{
            background-color: #e3f2fd;
        }}
        .answer-box {{
            margin-top: 25px;
            font-size: 16px;
        }}
        .answer-input {{
            width: 80px;
            padding: 8px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">What is the mode of the numbers?</div>
        
        <table class="table">
            <tr>
                <th>Month</th>
                <th>Hours</th>
            </tr>
            <tr><td>January</td><td>85</td></tr>
            <tr><td>February</td><td>74</td></tr>
            <tr><td>March</td><td>85</td></tr>
            <tr><td>April</td><td>85</td></tr>
            <tr><td>May</td><td>74</td></tr>
            <tr><td>June</td><td>79</td></tr>
            <tr><td>July</td><td>79</td></tr>
            <tr><td>August</td><td>85</td></tr>
        </table>
        
        <div class="answer-box">
            Mode = <input type="text" class="answer-input">
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_43_E2_{question_num}.html"

def create_gr6_44_e1_html(quiz):
    """Create HTML for histogram interpretation"""
    question_num = quiz['question_number']
    choices = quiz.get('choices', [])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Histogram</title>
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
            color: #333;
        }}
        .histogram {{
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .bar {{
            display: inline-block;
            width: 60px;
            background: #4CAF50;
            margin: 0 5px;
            vertical-align: bottom;
        }}
        .choices {{
            margin: 25px 0;
            text-align: left;
        }}
        .choice {{
            margin: 10px 0;
            padding: 10px 15px;
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
        }}
        .choice:hover {{
            background: #e3f2fd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">Which range occurred most frequently?</div>
        
        <div class="histogram">
            <div style="height: 200px; display: flex; align-items: flex-end; justify-content: center;">
                <div class="bar" style="height: 70px;"></div>
                <div class="bar" style="height: 140px;"></div>
                <div class="bar" style="height: 100px;"></div>
                <div class="bar" style="height: 80px;"></div>
                <div class="bar" style="height: 70px;"></div>
            </div>
            <div style="margin-top: 10px;">
                <span style="margin: 0 20px;">1-20</span>
                <span style="margin: 0 20px;">21-40</span>
                <span style="margin: 0 20px;">41-60</span>
                <span style="margin: 0 20px;">61-80</span>
                <span style="margin: 0 20px;">81-100</span>
            </div>
        </div>
        
        <div class="choices">"""
    
    for i, choice in enumerate(choices[:4]):
        html += f"""
            <div class="choice">{chr(65+i)}) {choice}</div>"""
    
    html += """
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_44_E1_{question_num}.html"

def create_gr6_44_e2_html(quiz):
    """Create HTML for line graph interpretation"""
    question_num = quiz['question_number']
    choices = quiz.get('choices', [])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Line Graph</title>
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
            color: #333;
        }}
        .graph {{
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .choices {{
            margin: 25px 0;
            text-align: left;
        }}
        .choice {{
            margin: 10px 0;
            padding: 10px 15px;
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
        }}
        .choice:hover {{
            background: #e3f2fd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">On which day did they have the fewest?</div>
        
        <div class="graph">
            <svg width="400" height="250" viewBox="0 0 400 250">
                <!-- Axes -->
                <line x1="40" y1="210" x2="360" y2="210" stroke="#333" stroke-width="2"/>
                <line x1="40" y1="30" x2="40" y2="210" stroke="#333" stroke-width="2"/>
                
                <!-- Line graph -->
                <polyline points="80,100 140,60 200,90 260,80 320,170" 
                          fill="none" stroke="#4CAF50" stroke-width="2"/>
                
                <!-- Points -->
                <circle cx="80" cy="100" r="4" fill="#4CAF50"/>
                <circle cx="140" cy="60" r="4" fill="#4CAF50"/>
                <circle cx="200" cy="90" r="4" fill="#4CAF50"/>
                <circle cx="260" cy="80" r="4" fill="#4CAF50"/>
                <circle cx="320" cy="170" r="4" fill="#4CAF50"/>
                
                <!-- Labels -->
                <text x="80" y="230" text-anchor="middle" font-size="12">Mon</text>
                <text x="140" y="230" text-anchor="middle" font-size="12">Tue</text>
                <text x="200" y="230" text-anchor="middle" font-size="12">Wed</text>
                <text x="260" y="230" text-anchor="middle" font-size="12">Thu</text>
                <text x="320" y="230" text-anchor="middle" font-size="12">Fri</text>
            </svg>
        </div>
        
        <div class="choices">"""
    
    for i, choice in enumerate(choices[:4]):
        html += f"""
            <div class="choice">{chr(65+i)}) {choice}</div>"""
    
    html += """
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_44_E2_{question_num}.html"

def create_gr6_44_e3_html(quiz):
    """Create HTML for double line graph"""
    question_num = quiz['question_number']
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Double Line Graph</title>
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
            color: #333;
        }}
        .graph {{
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .legend {{
            margin-top: 15px;
        }}
        .legend-item {{
            display: inline-block;
            margin: 0 15px;
        }}
        .answer-box {{
            margin-top: 25px;
            font-size: 16px;
        }}
        .answer-input {{
            width: 80px;
            padding: 8px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">How many students in 2011?</div>
        
        <div class="graph">
            <svg width="400" height="250" viewBox="0 0 400 250">
                <!-- Axes -->
                <line x1="40" y1="210" x2="360" y2="210" stroke="#333" stroke-width="2"/>
                <line x1="40" y1="30" x2="40" y2="210" stroke="#333" stroke-width="2"/>
                
                <!-- Line 1 -->
                <polyline points="80,100 140,80 200,120 260,90 320,70" 
                          fill="none" stroke="#4CAF50" stroke-width="2"/>
                
                <!-- Line 2 -->
                <polyline points="80,140 140,110 200,100 260,120 320,130" 
                          fill="none" stroke="#ff6b35" stroke-width="2"/>
                
                <!-- Year labels -->
                <text x="80" y="230" text-anchor="middle" font-size="12">2009</text>
                <text x="140" y="230" text-anchor="middle" font-size="12">2010</text>
                <text x="200" y="230" text-anchor="middle" font-size="12">2011</text>
                <text x="260" y="230" text-anchor="middle" font-size="12">2012</text>
                <text x="320" y="230" text-anchor="middle" font-size="12">2013</text>
            </svg>
            
            <div class="legend">
                <span class="legend-item">
                    <span style="color: #4CAF50;">●</span> Line A
                </span>
                <span class="legend-item">
                    <span style="color: #ff6b35;">●</span> Line B
                </span>
            </div>
        </div>
        
        <div class="answer-box">
            Students = <input type="text" class="answer-input">
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/Gr6_44_E3_{question_num}.html"

def main():
    os.makedirs('HTML', exist_ok=True)
    
    # Process each JSON file
    files = [
        ('Gr6_42_E4_variations.json', create_gr6_42_e4_html),
        ('Gr6_43_E2_variations.json', create_gr6_43_e2_html),
        ('Gr6_44_E1_variations.json', create_gr6_44_e1_html),
        ('Gr6_44_E2_variations.json', create_gr6_44_e2_html),
        ('Gr6_44_E3_variations.json', create_gr6_44_e3_html)
    ]
    
    for json_file, create_func in files:
        print(f"\nProcessing {json_file}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for quiz in data['quizzes']:
            html_content, filename = create_func(quiz)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            count += 1
            print(f"Created {filename}")
        
        print(f"Created {count} files for {json_file}")

if __name__ == "__main__":
    main()