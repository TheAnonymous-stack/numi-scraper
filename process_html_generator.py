import json
import os
import re

def extract_number_from_range(desc):
    """Extract specific numbers from description text."""
    # Look for patterns like "position 13", "position -5", etc.
    pos_match = re.search(r'position (-?\d+)', desc)
    if pos_match:
        return int(pos_match.group(1))
    
    # Look for patterns like "blank box placed at position"
    blank_match = re.search(r'blank box placed at position (-?\d+)', desc)
    if blank_match:
        return int(blank_match.group(1))
    
    return None

def extract_range_from_description(desc):
    """Extract the number line range from description."""
    # Look for patterns like "from -20 to 20", "from -10 to 10"
    range_match = re.search(r'from (-?\d+) to (-?\d+)', desc)
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))
    return -10, 10  # default range

def generate_number_line_svg(min_val, max_val, blank_position):
    """Generate SVG for a number line with a blank at the specified position."""
    range_size = max_val - min_val
    svg_width = max(600, range_size * 15 + 100)  # Dynamic width based on range
    
    # Calculate positions
    line_start = 50
    line_end = svg_width - 50
    line_length = line_end - line_start
    
    def pos_to_x(value):
        return line_start + ((value - min_val) / range_size) * line_length
    
    svg_parts = [
        f'<svg height="120" viewBox="0 0 {svg_width} 120" width="{svg_width}">',
        f'<!-- Number line from {min_val} to {max_val} -->',
        f'<line stroke="#000" stroke-width="2" x1="{line_start}" x2="{line_end}" y1="60" y2="60"></line>',
        '',
        '<!-- Tick marks and labels -->',
        '<g stroke="#000" stroke-width="1" fill="#000" font-family="Arial" font-size="12" text-anchor="middle">'
    ]
    
    # Add major tick marks (every 5 units or adjust for smaller ranges)
    tick_interval = 5 if range_size > 20 else (2 if range_size > 10 else 1)
    
    for val in range(min_val, max_val + 1, tick_interval):
        x_pos = pos_to_x(val)
        svg_parts.extend([
            f'  <line x1="{x_pos:.1f}" x2="{x_pos:.1f}" y1="50" y2="70"></line>',
            f'  <text x="{x_pos:.1f}" y="85">{val}</text>'
        ])
    
    # Add small tick for blank position if it's not already marked
    if blank_position is not None and blank_position % tick_interval != 0:
        blank_x = pos_to_x(blank_position)
        svg_parts.append(f'  <line x1="{blank_x:.1f}" x2="{blank_x:.1f}" y1="55" y2="65"></line>')
    
    svg_parts.append('</g>')
    
    # Add blank box at the specified position
    if blank_position is not None:
        blank_x = pos_to_x(blank_position)
        svg_parts.append(f'<rect x="{blank_x - 10:.1f}" y="35" width="20" height="20" fill="white" stroke="#000" stroke-width="2"></rect>')
    
    svg_parts.append('</svg>')
    
    return '\n     '.join(svg_parts)

def create_html_content(svg_content, label):
    """Create complete HTML content with the given SVG."""
    return f'''<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>
   Grade 6 Math Exercise
  </title>
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
            max-width: 900px;
        }}
        .visual-element {{
            margin: 20px auto;
            display: inline-block;
            padding: 10px;
        }}
        .grid-container {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            align-items: center;
        }}
  </style>
 </head>
 <body>
  <div class="container">
   <div class="visual-element item" label="{label}">
    {svg_content}
   </div>
  </div>
 </body>
</html>'''

def process_json_file(json_file_path):
    """Process a single JSON file and update corresponding HTML files."""
    if not os.path.exists(json_file_path):
        print(f"Warning: {json_file_path} not found")
        return
    
    print(f"Processing {json_file_path}")
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'quizzes' not in data:
        print(f"No 'quizzes' key found in {json_file_path}")
        return
    
    # Extract grade, week, exercise from filename
    filename = os.path.basename(json_file_path)
    # Example: Gr6_1_E4_variations.json -> Gr6, 1, E4
    match = re.match(r'Gr(\d+)_(\d+)_E(\d+)_variations\.json', filename)
    if not match:
        print(f"Cannot parse filename: {filename}")
        return
    
    grade, week, exercise = match.groups()
    
    for quiz in data['quizzes']:
        if 'image_tag' not in quiz or 'backend_description' not in quiz:
            continue
            
        question_number = quiz.get('question_number', 'unknown')
        image_tag = quiz['image_tag']
        description = quiz['backend_description']
        
        # Extract information from description
        min_val, max_val = extract_range_from_description(description)
        blank_position = extract_number_from_range(description)
        
        if blank_position is None:
            print(f"Could not find blank position in: {description}")
            continue
        
        # Generate SVG
        svg_content = generate_number_line_svg(min_val, max_val, blank_position)
        
        # Create HTML content
        html_content = create_html_content(svg_content, image_tag)
        
        # Create filename: Gr6_1_E4_4_1.html
        html_filename = f"Gr{grade}_{week}_E{exercise}_{question_number}.html"
        html_path = os.path.join("HTML", html_filename)
        
        # Write HTML file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Updated {html_filename}")

def main():
    """Main function to process all specified JSON files."""
    json_files = [
        "Gr6_1_E4_variations.json",
        "Gr6_1_E5_variations.json", 
        "Gr6_2_E1_variations.json",
        "Gr6_3_E2_variations.json",
        "Gr6_3_E4_variations.json",
        "Gr6_5_E1_variations.json",
        "Gr6_15_E5_variations.json",
        "Gr6_16_E1_variations.json",
        "Gr6_23_E1_variations.json",
        "Gr6_23_E2_variations.json",
        "Gr6_23_E3_variations.json",
        "Gr6_24_E1_variations.json",
        "Gr6_24_E2_variations.json",
        "Gr6_24_E3_variations.json",
        "Gr6_28_E3_variations.json",
        "Gr6_33_E1_variations.json",
        "Gr6_33_E2_variations.json",
        "Gr6_34_E3_variations.json",
        "Gr6_35_E1_variations.json",
        "Gr6_36_E1_variations.json",
        "Gr6_42_E4_variations.json",
        "Gr6_43_E2_variations.json",
        "Gr6_44_E1_variations.json",
        "Gr6_44_E2_variations.json",
        "Gr6_44_E3_variations.json",
        "Gr6_54_E3_variations.json",
        "Gr6_55_E1_variations.json"
    ]
    
    for json_file in json_files:
        try:
            process_json_file(json_file)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()