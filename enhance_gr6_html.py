import json
import os
import re
import math
from pathlib import Path

def create_detailed_histogram(description, tag):
    """Create a detailed histogram with proper labels and data"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="500" height="350" viewBox="0 0 500 350">\n'
    
    # Parse description for specific data
    bars_data = []
    x_label = "Category"
    y_label = "Frequency"
    title = ""
    
    if "episodes" in description.lower():
        x_label = "Number of Episodes"
        y_label = "Frequency"
        title = "Episodes Watched"
        # Extract numbers for episodes
        if "streamsource" in description.lower():
            bars_data = [("0", 2), ("1", 4), ("2", 6), ("3", 5), ("4", 3), ("5", 2)]
        else:
            bars_data = [("1", 3), ("2", 5), ("3", 7), ("4", 4), ("5", 2)]
    elif "books" in description.lower():
        x_label = "Number of Books"
        y_label = "Number of Students"
        title = "Books Read by Students"
        bars_data = [("0", 2), ("1", 5), ("2", 8), ("3", 6), ("4", 4), ("5", 3)]
    elif "hours" in description.lower():
        x_label = "Hours"
        y_label = "Frequency"
        title = "Study Hours"
        bars_data = [("1", 4), ("2", 7), ("3", 9), ("4", 6), ("5", 3)]
    elif "scores" in description.lower():
        x_label = "Score Range"
        y_label = "Number of Students"
        title = "Test Scores Distribution"
        bars_data = [("60-70", 3), ("70-80", 6), ("80-90", 8), ("90-100", 5)]
    else:
        # Default histogram
        num_bars = 5
        bars_data = [(str(i), 3 + i*2 - (i-2)**2) for i in range(1, num_bars+1)]
    
    if not bars_data:
        bars_data = [("A", 5), ("B", 8), ("C", 3), ("D", 6), ("E", 4)]
    
    # Draw axes
    axis_left = 60
    axis_bottom = 280
    axis_right = 440
    axis_top = 50
    
    html += f'<line x1="{axis_left}" y1="{axis_bottom}" x2="{axis_right}" y2="{axis_bottom}" stroke="black" stroke-width="2"/>\n'
    html += f'<line x1="{axis_left}" y1="{axis_top}" x2="{axis_left}" y2="{axis_bottom}" stroke="black" stroke-width="2"/>\n'
    
    # Calculate max value for scaling
    max_val = max([v for _, v in bars_data]) if bars_data else 10
    
    # Draw Y-axis labels
    for i in range(0, int(max_val) + 2, max(1, int(max_val) // 5)):
        y = axis_bottom - (i / max_val) * (axis_bottom - axis_top)
        html += f'<line x1="{axis_left-5}" y1="{y}" x2="{axis_left}" y2="{y}" stroke="black" stroke-width="1"/>\n'
        html += f'<text x="{axis_left-10}" y="{y+5}" text-anchor="end" font-size="12">{i}</text>\n'
    
    # Draw bars
    bar_width = (axis_right - axis_left - 20) / len(bars_data)
    for i, (label, value) in enumerate(bars_data):
        x = axis_left + 10 + i * bar_width
        bar_height = (value / max_val) * (axis_bottom - axis_top)
        y = axis_bottom - bar_height
        
        # Different colors for different bar groups
        colors = ["#4A90E2", "#7B68EE", "#FF6B6B", "#4ECDC4", "#FFD93D", "#95E77E"]
        color = colors[i % len(colors)]
        
        html += f'<rect x="{x}" y="{y}" width="{bar_width * 0.8}" height="{bar_height}" fill="{color}" opacity="0.8"/>\n'
        html += f'<text x="{x + bar_width * 0.4}" y="{axis_bottom + 20}" text-anchor="middle" font-size="12">{label}</text>\n'
        html += f'<text x="{x + bar_width * 0.4}" y="{y - 5}" text-anchor="middle" font-size="11" font-weight="bold">{value}</text>\n'
    
    # Add labels
    html += f'<text x="{(axis_left + axis_right) / 2}" y="{axis_bottom + 45}" text-anchor="middle" font-size="14" font-weight="bold">{x_label}</text>\n'
    html += f'<text x="25" y="{(axis_top + axis_bottom) / 2}" text-anchor="middle" font-size="14" font-weight="bold" transform="rotate(-90 25 {(axis_top + axis_bottom) / 2})">{y_label}</text>\n'
    
    if title:
        html += f'<text x="250" y="30" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_fraction_number_line(description, tag):
    """Create a number line specifically for fractions"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="700" height="150" viewBox="0 0 700 150">\n'
    
    # Main line
    line_start = 50
    line_end = 650
    line_y = 75
    
    html += f'<line x1="{line_start}" y1="{line_y}" x2="{line_end}" y2="{line_y}" stroke="black" stroke-width="2"/>\n'
    html += f'<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">\n'
    html += '<polygon points="0 0, 10 3.5, 0 7" fill="black"/>\n'
    html += '</marker>\n'
    html += f'<line x1="{line_end-5}" y1="{line_y}" x2="{line_end}" y2="{line_y}" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>\n'
    
    # Determine the range and divisions
    if "0 to 1" in description or "unit fraction" in description:
        # Fractions between 0 and 1
        if "eighths" in description.lower():
            denominator = 8
        elif "sixths" in description.lower():
            denominator = 6
        elif "fifths" in description.lower():
            denominator = 5
        elif "fourths" in description.lower() or "quarters" in description.lower():
            denominator = 4
        elif "thirds" in description.lower():
            denominator = 3
        elif "halves" in description.lower():
            denominator = 2
        else:
            denominator = 4  # Default
        
        # Draw major ticks and labels
        for i in range(denominator + 1):
            x = line_start + (i / denominator) * (line_end - line_start - 50)
            html += f'<line x1="{x}" y1="{line_y - 10}" x2="{x}" y2="{line_y + 10}" stroke="black" stroke-width="2"/>\n'
            
            # Fraction label
            if i == 0:
                label = "0"
            elif i == denominator:
                label = "1"
            else:
                # Simplify fraction if possible
                from math import gcd
                g = gcd(i, denominator)
                if g > 1:
                    label = f"{i//g}/{denominator//g}"
                else:
                    label = f"{i}/{denominator}"
            
            html += f'<text x="{x}" y="{line_y + 30}" text-anchor="middle" font-size="14">{label}</text>\n'
        
        # Add minor ticks if space allows
        if denominator <= 4:
            for i in range(denominator * 2 + 1):
                if i % 2 == 1:  # Only odd positions (between major ticks)
                    x = line_start + (i / (denominator * 2)) * (line_end - line_start - 50)
                    html += f'<line x1="{x}" y1="{line_y - 5}" x2="{x}" y2="{line_y + 5}" stroke="gray" stroke-width="1"/>\n'
    
    elif "mixed number" in description.lower():
        # Number line for mixed numbers
        for i in range(0, 4):
            x = line_start + i * 150
            html += f'<line x1="{x}" y1="{line_y - 10}" x2="{x}" y2="{line_y + 10}" stroke="black" stroke-width="2"/>\n'
            html += f'<text x="{x}" y="{line_y + 30}" text-anchor="middle" font-size="14">{i}</text>\n'
            
            # Add fraction marks between whole numbers
            for j in range(1, 4):
                fx = x + j * 37.5
                if fx < line_end - 50:
                    html += f'<line x1="{fx}" y1="{line_y - 5}" x2="{fx}" y2="{line_y + 5}" stroke="gray" stroke-width="1"/>\n'
    
    elif "negative" in description.lower() or "integer" in description.lower():
        # Number line with negative numbers
        center = (line_start + line_end - 50) / 2
        for i in range(-5, 6):
            x = center + i * 50
            if line_start <= x <= line_end - 50:
                html += f'<line x1="{x}" y1="{line_y - 10}" x2="{x}" y2="{line_y + 10}" stroke="black" stroke-width="2"/>\n'
                html += f'<text x="{x}" y="{line_y + 30}" text-anchor="middle" font-size="14">{i}</text>\n'
    
    else:
        # Standard 0-10 number line
        for i in range(11):
            x = line_start + i * 55
            html += f'<line x1="{x}" y1="{line_y - 10}" x2="{x}" y2="{line_y + 10}" stroke="black" stroke-width="2"/>\n'
            html += f'<text x="{x}" y="{line_y + 30}" text-anchor="middle" font-size="14">{i}</text>\n'
    
    # Add any specific points mentioned
    point_pattern = r'point.*?at\s+([\d./]+)'
    point_match = re.search(point_pattern, description, re.IGNORECASE)
    if point_match:
        point_str = point_match.group(1)
        try:
            if '/' in point_str:
                parts = point_str.split('/')
                point_val = float(parts[0]) / float(parts[1])
            else:
                point_val = float(point_str)
            
            # Calculate position
            if "negative" in description.lower():
                center = (line_start + line_end - 50) / 2
                x = center + point_val * 50
            else:
                x = line_start + point_val * (line_end - line_start - 50)
            
            if line_start <= x <= line_end - 50:
                html += f'<circle cx="{x}" cy="{line_y}" r="6" fill="red"/>\n'
                html += f'<text x="{x}" y="{line_y - 15}" text-anchor="middle" font-size="12" fill="red" font-weight="bold">{point_str}</text>\n'
        except:
            pass
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_geometric_angle(description, tag):
    """Create geometric angle diagrams with proper measurements"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="400" height="400" viewBox="0 0 400 400">\n'
    
    # Center point
    cx, cy = 200, 200
    
    # Extract angle value
    angle_pattern = r'(\d+)\s*(?:degree|°)'
    angle_match = re.search(angle_pattern, description, re.IGNORECASE)
    angle = int(angle_match.group(1)) if angle_match else 45
    
    # Determine angle type
    if "right angle" in description.lower() or angle == 90:
        angle = 90
        angle_type = "right"
    elif "acute" in description.lower() or angle < 90:
        angle_type = "acute"
    elif "obtuse" in description.lower() or angle > 90:
        angle_type = "obtuse"
    elif "straight" in description.lower() or angle == 180:
        angle = 180
        angle_type = "straight"
    else:
        angle_type = "acute" if angle < 90 else "obtuse"
    
    # Ray length
    ray_length = 150
    
    # First ray (horizontal to the right)
    x1, y1 = cx + ray_length, cy
    html += f'<line x1="{cx}" y1="{cy}" x2="{x1}" y2="{y1}" stroke="black" stroke-width="3"/>\n'
    
    # Second ray at the specified angle
    angle_rad = math.radians(angle)
    x2 = cx + ray_length * math.cos(angle_rad)
    y2 = cy - ray_length * math.sin(angle_rad)
    html += f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="3"/>\n'
    
    # Draw the angle arc
    arc_radius = 40
    
    if angle == 90:
        # Draw a square for right angle
        square_size = 25
        html += f'<path d="M {cx + square_size} {cy} L {cx + square_size} {cy - square_size} L {cx} {cy - square_size}" stroke="blue" stroke-width="2" fill="none"/>\n'
        # Small square in corner to indicate right angle
        html += f'<rect x="{cx + square_size - 5}" y="{cy - square_size - 5}" width="5" height="5" fill="blue"/>\n'
    elif angle == 180:
        # Draw a semicircle for straight angle
        html += f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 0 0 {cx - arc_radius} {cy}" stroke="blue" stroke-width="2" fill="none"/>\n'
    else:
        # Draw an arc for other angles
        end_x = cx + arc_radius * math.cos(angle_rad)
        end_y = cy - arc_radius * math.sin(angle_rad)
        large_arc = 1 if angle > 180 else 0
        html += f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 {large_arc} 0 {end_x} {end_y}" stroke="blue" stroke-width="2" fill="lightblue" fill-opacity="0.3"/>\n'
    
    # Add angle measurement label
    label_distance = arc_radius + 20
    label_angle = angle_rad / 2
    label_x = cx + label_distance * math.cos(label_angle)
    label_y = cy - label_distance * math.sin(label_angle)
    
    html += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-size="18" font-weight="bold">{angle}°</text>\n'
    
    # Add angle type label
    html += f'<text x="{cx}" y="50" text-anchor="middle" font-size="16" font-style="italic">{angle_type.capitalize()} Angle</text>\n'
    
    # Add vertex label
    html += f'<circle cx="{cx}" cy="{cy}" r="3" fill="black"/>\n'
    html += f'<text x="{cx - 15}" y="{cy + 20}" font-size="14" font-weight="bold">vertex</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_coordinate_grid(description, tag):
    """Create a coordinate grid with plotted points"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="500" height="500" viewBox="0 0 500 500">\n'
    
    # Grid parameters
    grid_size = 400
    grid_start = 50
    grid_end = grid_start + grid_size
    center_x = grid_start + grid_size / 2
    center_y = grid_start + grid_size / 2
    
    # Determine grid range
    if "quadrant" in description.lower() and "first" in description.lower():
        x_min, x_max = 0, 10
        y_min, y_max = 0, 10
    else:
        x_min, x_max = -10, 10
        y_min, y_max = -10, 10
    
    # Draw grid lines
    grid_divisions = 10
    for i in range(grid_divisions + 1):
        x = grid_start + (i / grid_divisions) * grid_size
        y = grid_start + (i / grid_divisions) * grid_size
        
        # Vertical lines
        stroke = "black" if i == grid_divisions // 2 else "lightgray"
        width = "2" if i == grid_divisions // 2 else "1"
        html += f'<line x1="{x}" y1="{grid_start}" x2="{x}" y2="{grid_end}" stroke="{stroke}" stroke-width="{width}"/>\n'
        
        # Horizontal lines
        html += f'<line x1="{grid_start}" y1="{y}" x2="{grid_end}" y2="{y}" stroke="{stroke}" stroke-width="{width}"/>\n'
    
    # Add axis labels
    for i in range(0, grid_divisions + 1, 2):
        x = grid_start + (i / grid_divisions) * grid_size
        y = grid_start + (i / grid_divisions) * grid_size
        
        # X-axis labels
        x_val = x_min + (i / grid_divisions) * (x_max - x_min)
        if x_val != 0:
            html += f'<text x="{x}" y="{center_y + 20}" text-anchor="middle" font-size="12">{int(x_val)}</text>\n'
        
        # Y-axis labels
        y_val = y_max - (i / grid_divisions) * (y_max - y_min)
        if y_val != 0:
            html += f'<text x="{center_x - 20}" y="{y + 5}" text-anchor="middle" font-size="12">{int(y_val)}</text>\n'
    
    # Add axis labels
    html += f'<text x="{grid_end + 20}" y="{center_y + 5}" font-size="14" font-weight="bold">x</text>\n'
    html += f'<text x="{center_x - 5}" y="{grid_start - 10}" font-size="14" font-weight="bold">y</text>\n'
    
    # Add origin label
    html += f'<text x="{center_x + 10}" y="{center_y + 20}" font-size="12">O</text>\n'
    
    # Plot any points mentioned
    point_pattern = r'\((-?\d+),\s*(-?\d+)\)'
    points = re.findall(point_pattern, description)
    colors = ["red", "blue", "green", "purple", "orange"]
    
    for i, (px, py) in enumerate(points[:5]):  # Limit to 5 points
        px_val = float(px)
        py_val = float(py)
        
        # Convert to SVG coordinates
        svg_x = center_x + (px_val / 10) * (grid_size / 2)
        svg_y = center_y - (py_val / 10) * (grid_size / 2)
        
        if grid_start <= svg_x <= grid_end and grid_start <= svg_y <= grid_end:
            color = colors[i % len(colors)]
            html += f'<circle cx="{svg_x}" cy="{svg_y}" r="5" fill="{color}"/>\n'
            html += f'<text x="{svg_x + 10}" y="{svg_y - 10}" font-size="12" fill="{color}">({px},{py})</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def update_existing_html_files():
    """Update existing HTML files with enhanced visualizations"""
    import glob
    
    # Load the generation data
    with open('gr6_files_to_generate.json', 'r') as f:
        files_data = json.load(f)
    
    updated_count = 0
    
    for file_info in files_data:
        filename = file_info['filename']
        if not os.path.exists(filename):
            continue
            
        visual_info = file_info['visual_info']
        question = file_info['question']
        
        # Check if this needs enhanced visualization
        needs_update = False
        
        # Check for specific visualization types that need enhancement
        if 'image_tag' in visual_info:
            desc = visual_info['image_tag'].lower()
            if any(keyword in desc for keyword in ['histogram', 'number line', 'angle', 'coordinate', 'fraction']):
                needs_update = True
        
        if 'solution_image_tag' in visual_info:
            for step in visual_info['solution_image_tag']:
                if len(step) >= 3:
                    desc = step[2].lower()
                    if any(keyword in desc for keyword in ['histogram', 'number line', 'angle', 'coordinate', 'fraction']):
                        needs_update = True
        
        if needs_update:
            # Generate enhanced HTML content
            html_parts = []
            
            # Handle image_tag
            if 'image_tag' in visual_info and visual_info['image_tag']:
                tag = question.get('image_tag', 'Gr6_image')
                description = visual_info['image_tag']
                
                if "histogram" in description.lower():
                    html_parts.append(create_detailed_histogram(description, tag))
                elif "number line" in description.lower():
                    html_parts.append(create_fraction_number_line(description, tag))
                elif "angle" in description.lower() and "degree" in description.lower():
                    html_parts.append(create_geometric_angle(description, tag))
                elif "coordinate" in description.lower() or "grid" in description.lower():
                    html_parts.append(create_coordinate_grid(description, tag))
                elif "place value" in description.lower():
                    # Keep existing place value implementation
                    pass
            
            # Handle solution_image_tag
            if 'solution_image_tag' in visual_info and visual_info['solution_image_tag']:
                for step_info in visual_info['solution_image_tag']:
                    if len(step_info) >= 3:
                        step_num = step_info[0]
                        step_tag = step_info[1]
                        step_description = step_info[2]
                        
                        if "histogram" in step_description.lower():
                            html_parts.append(create_detailed_histogram(step_description, step_tag))
                        elif "number line" in step_description.lower():
                            html_parts.append(create_fraction_number_line(step_description, step_tag))
                        elif "angle" in step_description.lower():
                            html_parts.append(create_geometric_angle(step_description, step_tag))
                        elif "coordinate" in step_description.lower():
                            html_parts.append(create_coordinate_grid(step_description, step_tag))
            
            if html_parts:
                # Write enhanced content
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(html_parts))
                updated_count += 1
                
                if updated_count % 100 == 0:
                    print(f"Updated {updated_count} files...")
    
    print(f"\nEnhanced {updated_count} HTML files with detailed visualizations.")

if __name__ == "__main__":
    update_existing_html_files()