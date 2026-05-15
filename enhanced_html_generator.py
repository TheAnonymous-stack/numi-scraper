import json
import os
import re
import math

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

def extract_grid_info(desc):
    """Extract grid information from description."""
    # Look for patterns like "91 squares are shaded out of the 100 squares"
    shaded_match = re.search(r'(\d+) squares are shaded out of the (\d+) squares', desc)
    if shaded_match:
        return int(shaded_match.group(1)), int(shaded_match.group(2))
    return None, None

def extract_fraction_info(desc):
    """Extract fraction information from description."""
    # Look for division patterns like "divided into 2 equal parts", "divided into 4 equal parts"
    division_match = re.search(r'divided into (\d+) equal parts', desc)
    if division_match:
        parts = int(division_match.group(1))
        # Look for shaded parts
        if "bottom half shaded" in desc:
            shaded = 1
        elif "bottom-left quarter shaded" in desc:
            shaded = 1
        else:
            shaded = 1  # default
        return shaded, parts
    
    # Look for grid patterns like "2 columns and 5 rows, making 10 equal parts, with 9 of them shaded"
    grid_match = re.search(r'(\d+) columns and (\d+) rows, making (\d+) equal parts, with (\d+) of them shaded', desc)
    if grid_match:
        cols = int(grid_match.group(1))
        rows = int(grid_match.group(2))
        total = int(grid_match.group(3))
        shaded = int(grid_match.group(4))
        return shaded, total, cols, rows
    
    return None

def generate_number_line_svg(min_val, max_val, blank_position):
    """Generate SVG for a number line with a blank at the specified position."""
    range_size = max_val - min_val
    svg_width = max(600, range_size * 15 + 100)
    
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
    
    # Add major tick marks
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

def generate_grid_svg(shaded1, total1, shaded2=None, total2=None):
    """Generate SVG for decimal grids (100-square grids)."""
    svg_width = 420 if shaded2 is not None else 220
    
    svg_parts = [
        f'<svg height="240" viewBox="0 0 {svg_width} 240" width="{svg_width}">',
        '<!-- Decimal grids -->'
    ]
    
    # First grid
    svg_parts.append('<g id="grid1">')
    for i in range(10):
        for j in range(10):
            x = 10 + j * 20
            y = 10 + i * 20
            square_num = i * 10 + j
            fill_color = "#4CAF50" if square_num < shaded1 else "white"
            stroke_color = "#000"
            svg_parts.append(f'  <rect x="{x}" y="{y}" width="18" height="18" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"></rect>')
    svg_parts.append('</g>')
    
    # Second grid if provided
    if shaded2 is not None and total2 is not None:
        svg_parts.append('<g id="grid2">')
        for i in range(10):
            for j in range(10):
                x = 220 + j * 20
                y = 10 + i * 20
                square_num = i * 10 + j
                fill_color = "#2196F3" if square_num < shaded2 else "white"
                stroke_color = "#000"
                svg_parts.append(f'  <rect x="{x}" y="{y}" width="18" height="18" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"></rect>')
        svg_parts.append('</g>')
    
    svg_parts.append('</svg>')
    return '\n     '.join(svg_parts)

def generate_fraction_svg(description):
    """Generate SVG for fraction representations."""
    # Handle different fraction types
    if "square divided into 2 equal parts" in description and "square divided into 4 equal parts" in description:
        # Two shapes side by side
        svg_parts = [
            '<svg height="200" viewBox="0 0 400 200" width="400">',
            '<!-- Two fraction shapes -->',
            '<!-- First shape: halves -->',
            '<g id="shape1">',
            '  <rect x="50" y="50" width="100" height="100" fill="white" stroke="#000" stroke-width="2"></rect>',
            '  <line x1="50" x2="150" y1="100" y2="100" stroke="#000" stroke-width="1"></line>',
            '  <rect x="50" y="100" width="100" height="50" fill="#4CAF50"></rect>',
            '</g>',
            '<!-- Second shape: quarters -->',
            '<g id="shape2">',
            '  <rect x="250" y="50" width="100" height="100" fill="white" stroke="#000" stroke-width="2"></rect>',
            '  <line x1="250" x2="350" y1="100" y2="100" stroke="#000" stroke-width="1"></line>',
            '  <line x1="300" x2="300" y1="50" y2="150" stroke="#000" stroke-width="1"></line>',
            '  <rect x="250" y="100" width="50" height="50" fill="#4CAF50"></rect>',
            '</g>',
            '</svg>'
        ]
        return '\n     '.join(svg_parts)
    
    elif "columns and" in description and "rows" in description:
        # Grid-based fractions
        grid_info = extract_fraction_info(description)
        if grid_info and len(grid_info) == 4:
            shaded, total, cols, rows = grid_info
            cell_width = 20
            cell_height = 20
            svg_width = cols * cell_width + 100
            svg_height = rows * cell_height + 100
            
            svg_parts = [
                f'<svg height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}">',
                '<!-- Grid-based fraction -->'
            ]
            
            shaded_count = 0
            for i in range(rows):
                for j in range(cols):
                    x = 50 + j * cell_width
                    y = 50 + i * cell_height
                    fill_color = "#4CAF50" if shaded_count < shaded else "white"
                    svg_parts.append(f'  <rect x="{x}" y="{y}" width="{cell_width-2}" height="{cell_height-2}" fill="{fill_color}" stroke="#000" stroke-width="1"></rect>')
                    shaded_count += 1
            
            svg_parts.append('</svg>')
            return '\n     '.join(svg_parts)
    
    # Default fraction representation
    return '<svg height="150" viewBox="0 0 300 150" width="300"><rect x="50" y="25" width="200" height="100" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="10"></rect><text x="150" y="85" text-anchor="middle" font-family="Arial" font-size="18" fill="#1976D2">Fraction Model</text></svg>'

def generate_even_number_line_svg(min_val, max_val):
    """Generate SVG for number lines showing only even numbers."""
    range_size = max_val - min_val
    svg_width = max(600, range_size * 8 + 100)
    
    line_start = 50
    line_end = svg_width - 50
    line_length = line_end - line_start
    
    def pos_to_x(value):
        return line_start + ((value - min_val) / range_size) * line_length
    
    svg_parts = [
        f'<svg height="120" viewBox="0 0 {svg_width} 120" width="{svg_width}">',
        f'<!-- Number line from {min_val} to {max_val} (even numbers only) -->',
        f'<line stroke="#000" stroke-width="2" x1="{line_start}" x2="{line_end}" y1="60" y2="60"></line>',
        '',
        '<!-- Tick marks and labels for even numbers -->',
        '<g stroke="#000" stroke-width="1" fill="#000" font-family="Arial" font-size="12" text-anchor="middle">'
    ]
    
    # Add tick marks only for even numbers
    for val in range(min_val, max_val + 1):
        if val % 2 == 0:  # Only even numbers
            x_pos = pos_to_x(val)
            svg_parts.extend([
                f'  <line x1="{x_pos:.1f}" x2="{x_pos:.1f}" y1="50" y2="70"></line>',
                f'  <text x="{x_pos:.1f}" y="85">{val}</text>'
            ])
        else:
            # Small tick marks for odd numbers (unlabeled)
            x_pos = pos_to_x(val)
            svg_parts.append(f'  <line x1="{x_pos:.1f}" x2="{x_pos:.1f}" y1="55" y2="65"></line>')
    
    svg_parts.append('</g>')
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
            max-width: 1000px;
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

def determine_visual_type(description):
    """Determine what type of visual representation is needed."""
    desc_lower = description.lower()
    
    if "blank box placed at position" in desc_lower and "number line" in desc_lower:
        return "number_line_blank"
    elif "only the even numbers are labeled" in desc_lower and "number line" in desc_lower:
        return "even_number_line"
    elif "squares are shaded out of the 100 squares" in desc_lower:
        return "decimal_grids"
    elif "divided into" in desc_lower and "equal parts" in desc_lower:
        return "fractions"
    else:
        return "unknown"

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
    match = re.match(r'Gr(\d+)_(\d+)_E(\d+)_variations\.json', filename)
    if not match:
        print(f"Cannot parse filename: {filename}")
        return
    
    grade, week, exercise = match.groups()
    
    processed_count = 0
    for quiz in data['quizzes']:
        if 'image_tag' not in quiz or 'backend_description' not in quiz:
            continue
            
        question_number = quiz.get('question_number', 'unknown')
        image_tag = quiz['image_tag']
        description = quiz['backend_description']
        
        visual_type = determine_visual_type(description)
        svg_content = None
        
        if visual_type == "number_line_blank":
            min_val, max_val = extract_range_from_description(description)
            blank_position = extract_number_from_range(description)
            if blank_position is not None:
                svg_content = generate_number_line_svg(min_val, max_val, blank_position)
        
        elif visual_type == "even_number_line":
            min_val, max_val = extract_range_from_description(description)
            svg_content = generate_even_number_line_svg(min_val, max_val)
        
        elif visual_type == "decimal_grids":
            # Extract both grid information for comparison questions
            descriptions = description.split("In the first grid,")
            if len(descriptions) > 1:
                # First grid
                first_desc = descriptions[1].split("In the second grid,")[0]
                shaded1, total1 = extract_grid_info("In the first grid," + first_desc)
                
                # Second grid
                if "In the second grid," in description:
                    second_desc = description.split("In the second grid,")[1]
                    shaded2, total2 = extract_grid_info("In the second grid," + second_desc)
                    if shaded1 and shaded2:
                        svg_content = generate_grid_svg(shaded1, total1, shaded2, total2)
                else:
                    if shaded1:
                        svg_content = generate_grid_svg(shaded1, total1)
        
        elif visual_type == "fractions":
            svg_content = generate_fraction_svg(description)
        
        if svg_content:
            html_content = create_html_content(svg_content, image_tag)
            html_filename = f"Gr{grade}_{week}_E{exercise}_{question_number}.html"
            html_path = os.path.join("HTML", html_filename)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            processed_count += 1
            print(f"  Updated {html_filename}")
        else:
            print(f"  Could not generate visual for: {description[:100]}...")
    
    print(f"  Processed {processed_count} files from {filename}")

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
    
    total_processed = 0
    for json_file in json_files:
        try:
            process_json_file(json_file)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()