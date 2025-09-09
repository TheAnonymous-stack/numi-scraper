import json
import os
import re
import math
from pathlib import Path

def create_fraction_model(description, tag):
    """Create fraction models (circles, rectangles, etc.)"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="400" height="400" viewBox="0 0 400 400">\n'
    
    # Determine shape type and fraction
    if "circle" in description.lower() or "pie" in description.lower():
        # Circular fraction model
        cx, cy, r = 200, 200, 100
        
        # Extract fraction
        frac_match = re.search(r'(\d+)/(\d+)', description)
        if frac_match:
            numerator = int(frac_match.group(1))
            denominator = int(frac_match.group(2))
        else:
            numerator, denominator = 1, 4
        
        # Draw the circle
        html += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="black" stroke-width="2"/>\n'
        
        # Draw sectors
        angle_per_sector = 360 / denominator
        for i in range(denominator):
            start_angle = i * angle_per_sector - 90
            end_angle = start_angle + angle_per_sector
            
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            x1 = cx + r * math.cos(start_rad)
            y1 = cy + r * math.sin(start_rad)
            x2 = cx + r * math.cos(end_rad)
            y2 = cy + r * math.sin(end_rad)
            
            # Color the numerator portions
            fill_color = "#4A90E2" if i < numerator else "white"
            
            large_arc = 0 if angle_per_sector <= 180 else 1
            
            html += f'<path d="M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2} Z" '
            html += f'fill="{fill_color}" stroke="black" stroke-width="1" fill-opacity="0.8"/>\n'
        
        # Add fraction label
        html += f'<text x="{cx}" y="350" text-anchor="middle" font-size="20" font-weight="bold">{numerator}/{denominator}</text>\n'
    
    elif "rectangle" in description.lower() or "bar" in description.lower():
        # Rectangular fraction model
        rect_width = 300
        rect_height = 100
        x_start = 50
        y_start = 150
        
        # Extract fraction
        frac_match = re.search(r'(\d+)/(\d+)', description)
        if frac_match:
            numerator = int(frac_match.group(1))
            denominator = int(frac_match.group(2))
        else:
            numerator, denominator = 1, 4
        
        # Draw the rectangle divided into parts
        part_width = rect_width / denominator
        
        for i in range(denominator):
            x = x_start + i * part_width
            fill_color = "#4A90E2" if i < numerator else "white"
            
            html += f'<rect x="{x}" y="{y_start}" width="{part_width}" height="{rect_height}" '
            html += f'fill="{fill_color}" stroke="black" stroke-width="2" fill-opacity="0.8"/>\n'
        
        # Add fraction label
        html += f'<text x="200" y="300" text-anchor="middle" font-size="20" font-weight="bold">{numerator}/{denominator}</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_area_model(description, tag):
    """Create area models for multiplication"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="500" height="500" viewBox="0 0 500 500">\n'
    
    # Extract numbers from description
    nums = re.findall(r'\d+', description)
    if len(nums) >= 2:
        num1, num2 = int(nums[0]), int(nums[1])
    else:
        num1, num2 = 12, 15
    
    # Break down numbers into parts
    parts1 = []
    parts2 = []
    
    if num1 >= 10:
        parts1 = [10 * (num1 // 10), num1 % 10] if num1 % 10 else [num1]
    else:
        parts1 = [num1]
    
    if num2 >= 10:
        parts2 = [10 * (num2 // 10), num2 % 10] if num2 % 10 else [num2]
    else:
        parts2 = [num2]
    
    # Calculate grid dimensions
    grid_x = 100
    grid_y = 100
    cell_size = 30
    
    # Draw labels for first number (top)
    x_pos = grid_x
    for part in parts1:
        width = cell_size * 2 if part >= 10 else cell_size
        html += f'<text x="{x_pos + width/2}" y="{grid_y - 10}" text-anchor="middle" font-size="16" font-weight="bold">{part}</text>\n'
        x_pos += width
    
    # Draw labels for second number (left)
    y_pos = grid_y
    for part in parts2:
        height = cell_size * 2 if part >= 10 else cell_size
        html += f'<text x="{grid_x - 30}" y="{y_pos + height/2 + 5}" text-anchor="middle" font-size="16" font-weight="bold">{part}</text>\n'
        y_pos += height
    
    # Draw the grid cells
    y_pos = grid_y
    colors = ["#FFE5B4", "#FFD4A3", "#FFC392", "#FFB281"]
    color_idx = 0
    
    for j, part2 in enumerate(parts2):
        x_pos = grid_x
        height = cell_size * 2 if part2 >= 10 else cell_size
        
        for i, part1 in enumerate(parts1):
            width = cell_size * 2 if part1 >= 10 else cell_size
            product = part1 * part2
            
            # Draw cell
            html += f'<rect x="{x_pos}" y="{y_pos}" width="{width}" height="{height}" '
            html += f'fill="{colors[color_idx % len(colors)]}" stroke="black" stroke-width="2"/>\n'
            
            # Add product in cell
            html += f'<text x="{x_pos + width/2}" y="{y_pos + height/2 + 5}" '
            html += f'text-anchor="middle" font-size="14" font-weight="bold">{product}</text>\n'
            
            x_pos += width
            color_idx += 1
        
        y_pos += height
    
    # Add total
    total = num1 * num2
    html += f'<text x="250" y="400" text-anchor="middle" font-size="20" font-weight="bold">'
    html += f'{num1} × {num2} = {total}</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_data_table(description, tag):
    """Create data tables and charts"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="600" height="400" viewBox="0 0 600 400">\n'
    
    # Determine table type from description
    if "frequency" in description.lower():
        # Frequency table
        headers = ["Value", "Frequency"]
        data = [
            ["1", "3"],
            ["2", "5"],
            ["3", "7"],
            ["4", "4"],
            ["5", "2"]
        ]
    elif "two-way" in description.lower():
        # Two-way table
        headers = ["", "Category A", "Category B", "Total"]
        data = [
            ["Group 1", "12", "8", "20"],
            ["Group 2", "15", "10", "25"],
            ["Total", "27", "18", "45"]
        ]
    else:
        # Generic data table
        headers = ["Item", "Count", "Percentage"]
        data = [
            ["A", "25", "25%"],
            ["B", "35", "35%"],
            ["C", "20", "20%"],
            ["D", "20", "20%"]
        ]
    
    # Calculate dimensions
    col_width = 120
    row_height = 40
    start_x = 50
    start_y = 50
    
    # Draw headers
    for i, header in enumerate(headers):
        x = start_x + i * col_width
        html += f'<rect x="{x}" y="{start_y}" width="{col_width}" height="{row_height}" '
        html += f'fill="#E0E0E0" stroke="black" stroke-width="1"/>\n'
        html += f'<text x="{x + col_width/2}" y="{start_y + row_height/2 + 5}" '
        html += f'text-anchor="middle" font-size="14" font-weight="bold">{header}</text>\n'
    
    # Draw data rows
    for row_idx, row in enumerate(data):
        y = start_y + (row_idx + 1) * row_height
        for col_idx, cell in enumerate(row):
            x = start_x + col_idx * col_width
            
            # Alternate row colors
            fill_color = "white" if row_idx % 2 == 0 else "#F5F5F5"
            
            html += f'<rect x="{x}" y="{y}" width="{col_width}" height="{row_height}" '
            html += f'fill="{fill_color}" stroke="black" stroke-width="1"/>\n'
            html += f'<text x="{x + col_width/2}" y="{y + row_height/2 + 5}" '
            html += f'text-anchor="middle" font-size="12">{cell}</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_geometric_shape(description, tag):
    """Create various geometric shapes with measurements"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="500" height="500" viewBox="0 0 500 500">\n'
    
    if "triangle" in description.lower():
        # Extract triangle type
        if "equilateral" in description.lower():
            # Equilateral triangle
            points = "250,100 150,273 350,273"
            html += f'<polygon points="{points}" fill="lightblue" stroke="black" stroke-width="2"/>\n'
            # Add side labels
            html += '<text x="200" y="190" font-size="12">60°</text>\n'
            html += '<text x="300" y="190" font-size="12">60°</text>\n'
            html += '<text x="250" y="290" font-size="12">60°</text>\n'
        elif "right" in description.lower():
            # Right triangle
            points = "150,150 350,150 350,350"
            html += f'<polygon points="{points}" fill="lightgreen" stroke="black" stroke-width="2"/>\n'
            # Add right angle indicator
            html += '<rect x="325" y="150" width="25" height="25" fill="none" stroke="black" stroke-width="1"/>\n'
            html += '<rect x="340" y="165" width="5" height="5" fill="black"/>\n'
        else:
            # Scalene triangle
            points = "200,120 120,320 380,280"
            html += f'<polygon points="{points}" fill="lightyellow" stroke="black" stroke-width="2"/>\n'
    
    elif "square" in description.lower():
        side = 200
        x = 150
        y = 150
        html += f'<rect x="{x}" y="{y}" width="{side}" height="{side}" fill="lightcoral" stroke="black" stroke-width="2"/>\n'
        # Add side length labels
        html += f'<text x="{x + side/2}" y="{y - 10}" text-anchor="middle" font-size="14">{side/10} cm</text>\n'
        html += f'<text x="{x - 30}" y="{y + side/2}" font-size="14">{side/10} cm</text>\n'
    
    elif "rectangle" in description.lower():
        width = 250
        height = 150
        x = 125
        y = 175
        html += f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="lightpink" stroke="black" stroke-width="2"/>\n'
        # Add dimension labels
        html += f'<text x="{x + width/2}" y="{y - 10}" text-anchor="middle" font-size="14">{width/10} cm</text>\n'
        html += f'<text x="{x - 30}" y="{y + height/2}" font-size="14">{height/10} cm</text>\n'
    
    elif "pentagon" in description.lower():
        # Regular pentagon
        cx, cy = 250, 250
        r = 100
        points = []
        for i in range(5):
            angle = -90 + i * 72  # Start from top
            x = cx + r * math.cos(math.radians(angle))
            y = cy + r * math.sin(math.radians(angle))
            points.append(f"{x},{y}")
        
        html += f'<polygon points="{" ".join(points)}" fill="lightsteelblue" stroke="black" stroke-width="2"/>\n'
    
    elif "hexagon" in description.lower():
        # Regular hexagon
        cx, cy = 250, 250
        r = 100
        points = []
        for i in range(6):
            angle = i * 60
            x = cx + r * math.cos(math.radians(angle))
            y = cy + r * math.sin(math.radians(angle))
            points.append(f"{x},{y}")
        
        html += f'<polygon points="{" ".join(points)}" fill="lavender" stroke="black" stroke-width="2"/>\n'
    
    elif "circle" in description.lower():
        cx, cy = 250, 250
        r = 100
        html += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="lightskyblue" stroke="black" stroke-width="2"/>\n'
        
        # Add radius or diameter if mentioned
        if "radius" in description.lower():
            html += f'<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="red" stroke-width="2"/>\n'
            html += f'<text x="{cx + r/2}" y="{cy - 10}" font-size="14">r = {r/10} cm</text>\n'
        elif "diameter" in description.lower():
            html += f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="red" stroke-width="2"/>\n'
            html += f'<text x="{cx}" y="{cy - 10}" text-anchor="middle" font-size="14">d = {r*2/10} cm</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_ratio_visual(description, tag):
    """Create ratio and proportion visualizations"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="600" height="300" viewBox="0 0 600 300">\n'
    
    # Extract ratio
    ratio_match = re.search(r'(\d+):(\d+)', description)
    if ratio_match:
        part1 = int(ratio_match.group(1))
        part2 = int(ratio_match.group(2))
    else:
        part1, part2 = 3, 2
    
    # Draw ratio bars
    total_parts = part1 + part2
    bar_height = 60
    unit_width = 400 / total_parts
    
    # First part
    x1 = 100
    y = 120
    width1 = part1 * unit_width
    html += f'<rect x="{x1}" y="{y}" width="{width1}" height="{bar_height}" fill="#4A90E2" stroke="black" stroke-width="2"/>\n'
    html += f'<text x="{x1 + width1/2}" y="{y + bar_height/2 + 5}" text-anchor="middle" font-size="20" fill="white" font-weight="bold">{part1}</text>\n'
    
    # Second part
    x2 = x1 + width1
    width2 = part2 * unit_width
    html += f'<rect x="{x2}" y="{y}" width="{width2}" height="{bar_height}" fill="#FF6B6B" stroke="black" stroke-width="2"/>\n'
    html += f'<text x="{x2 + width2/2}" y="{y + bar_height/2 + 5}" text-anchor="middle" font-size="20" fill="white" font-weight="bold">{part2}</text>\n'
    
    # Add ratio label
    html += f'<text x="300" y="80" text-anchor="middle" font-size="24" font-weight="bold">Ratio {part1}:{part2}</text>\n'
    
    # Add labels if mentioned in description
    if "boys" in description.lower() and "girls" in description.lower():
        html += f'<text x="{x1 + width1/2}" y="{y + bar_height + 30}" text-anchor="middle" font-size="16">Boys</text>\n'
        html += f'<text x="{x2 + width2/2}" y="{y + bar_height + 30}" text-anchor="middle" font-size="16">Girls</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def generate_all_html():
    """Generate all HTML files with comprehensive visualizations"""
    with open('gr6_files_to_generate.json', 'r') as f:
        files_data = json.load(f)
    
    total_files = len(files_data)
    generated_count = 0
    
    print(f"Generating {total_files} HTML files with comprehensive visualizations...")
    
    for i, file_info in enumerate(files_data):
        if i % 100 == 0:
            print(f"Progress: {i}/{total_files} files...")
        
        filename = file_info['filename']
        visual_info = file_info['visual_info']
        question = file_info['question']
        
        html_parts = []
        
        # Handle image_tag
        if 'image_tag' in visual_info and visual_info['image_tag']:
            tag = question.get('image_tag', f'Gr6_{file_info["question_num"]}_image')
            description = visual_info['image_tag']
            
            # Choose appropriate visualization
            if "histogram" in description.lower():
                from enhance_gr6_html import create_detailed_histogram
                html_parts.append(create_detailed_histogram(description, tag))
            elif "number line" in description.lower():
                from enhance_gr6_html import create_fraction_number_line
                html_parts.append(create_fraction_number_line(description, tag))
            elif "angle" in description.lower():
                from enhance_gr6_html import create_geometric_angle
                html_parts.append(create_geometric_angle(description, tag))
            elif "coordinate" in description.lower() or "grid" in description.lower():
                from enhance_gr6_html import create_coordinate_grid
                html_parts.append(create_coordinate_grid(description, tag))
            elif "fraction" in description.lower() or "shaded" in description.lower():
                html_parts.append(create_fraction_model(description, tag))
            elif "area model" in description.lower():
                html_parts.append(create_area_model(description, tag))
            elif "ratio" in description.lower():
                html_parts.append(create_ratio_visual(description, tag))
            elif "table" in description.lower() or "data" in description.lower():
                html_parts.append(create_data_table(description, tag))
            elif any(shape in description.lower() for shape in ["triangle", "square", "rectangle", "pentagon", "hexagon", "circle"]):
                html_parts.append(create_geometric_shape(description, tag))
            elif "place value" in description.lower():
                from generate_gr6_html import create_place_value_chart
                html_parts.append(create_place_value_chart(description, tag))
            elif "map" in description.lower():
                from generate_gr6_html import create_map_visualization
                html_parts.append(create_map_visualization(description, tag))
            else:
                from generate_gr6_html import create_generic_shape
                html_parts.append(create_generic_shape(description, tag))
        
        # Handle solution_image_tag
        if 'solution_image_tag' in visual_info and visual_info['solution_image_tag']:
            for step_info in visual_info['solution_image_tag']:
                if len(step_info) >= 3:
                    step_num = step_info[0]
                    step_tag = step_info[1]
                    step_description = step_info[2]
                    
                    # Choose appropriate visualization for solution step
                    if "histogram" in step_description.lower():
                        from enhance_gr6_html import create_detailed_histogram
                        html_parts.append(create_detailed_histogram(step_description, step_tag))
                    elif "number line" in step_description.lower():
                        from enhance_gr6_html import create_fraction_number_line
                        html_parts.append(create_fraction_number_line(step_description, step_tag))
                    elif "angle" in step_description.lower():
                        from enhance_gr6_html import create_geometric_angle
                        html_parts.append(create_geometric_angle(step_description, step_tag))
                    elif "coordinate" in step_description.lower():
                        from enhance_gr6_html import create_coordinate_grid
                        html_parts.append(create_coordinate_grid(step_description, step_tag))
                    elif "fraction" in step_description.lower():
                        html_parts.append(create_fraction_model(step_description, step_tag))
                    elif "area model" in step_description.lower():
                        html_parts.append(create_area_model(step_description, step_tag))
                    elif "ratio" in step_description.lower():
                        html_parts.append(create_ratio_visual(step_description, step_tag))
                    elif "place value" in step_description.lower():
                        from generate_gr6_html import create_place_value_chart
                        html_parts.append(create_place_value_chart(step_description, step_tag))
                    else:
                        from generate_gr6_html import create_generic_shape
                        html_parts.append(create_generic_shape(step_description, step_tag))
        
        # Handle image_choice_tags
        if 'image_choice_tags' in visual_info and visual_info['image_choice_tags']:
            tags = visual_info['image_choice_tags']
            descriptions = visual_info.get('image_choice_descriptions', [])
            
            for idx, tag in enumerate(tags):
                if idx < len(descriptions):
                    description = descriptions[idx]
                    
                    if "histogram" in description.lower():
                        from enhance_gr6_html import create_detailed_histogram
                        html_parts.append(create_detailed_histogram(description, tag))
                    elif "number line" in description.lower():
                        from enhance_gr6_html import create_fraction_number_line
                        html_parts.append(create_fraction_number_line(description, tag))
                    elif "fraction" in description.lower():
                        html_parts.append(create_fraction_model(description, tag))
                    elif any(shape in description.lower() for shape in ["triangle", "square", "circle"]):
                        html_parts.append(create_geometric_shape(description, tag))
                    else:
                        from generate_gr6_html import create_generic_shape
                        html_parts.append(create_generic_shape(description, tag))
        
        # Write HTML file
        if html_parts:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(html_parts))
            generated_count += 1
    
    print(f"\nCompleted! Generated {generated_count}/{total_files} HTML files.")

if __name__ == "__main__":
    generate_all_html()