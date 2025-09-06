import json
import os
import math
from pathlib import Path

def create_grid_svg(cols=20, rows=20, unit_size=25):
    """Create a coordinate grid SVG"""
    width = cols * unit_size
    height = rows * unit_size
    
    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px;">
    <!-- Grid lines -->
    <defs>
        <pattern id="grid" width="{unit_size}" height="{unit_size}" patternUnits="userSpaceOnUse">
            <path d="M {unit_size} 0 L 0 0 0 {unit_size}" fill="none" stroke="#e0e0e0" stroke-width="1"/>
        </pattern>
    </defs>
    
    <rect width="{width}" height="{height}" fill="white"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    
    <!-- Major axes -->
    <line x1="0" y1="{height}" x2="{width}" y2="{height}" stroke="#333" stroke-width="2"/>
    <line x1="0" y1="0" x2="0" y2="{height}" stroke="#333" stroke-width="2"/>
    '''
    
    return svg, width, height, unit_size

def add_shape_to_grid(svg, shape_type, x, y, size, color, rotation=0, transform_type=None):
    """Add a shape to the grid"""
    unit_size = 25
    cx = x * unit_size
    cy = y * unit_size
    shape_size = size * unit_size
    
    if shape_type == "square":
        shape = f'<rect x="{cx}" y="{cy}" width="{shape_size}" height="{shape_size}" '
    elif shape_type == "hexagon":
        # Create hexagon points
        points = []
        for i in range(6):
            angle = i * 60 - 30  # Start from top
            px = cx + shape_size/2 + shape_size/2 * math.cos(math.radians(angle))
            py = cy + shape_size/2 + shape_size/2 * math.sin(math.radians(angle))
            points.append(f"{px},{py}")
        shape = f'<polygon points="{" ".join(points)}" '
    elif shape_type == "triangle":
        # Create triangle points  
        points = [
            f"{cx + shape_size/2},{cy}",
            f"{cx},{cy + shape_size}",
            f"{cx + shape_size},{cy + shape_size}"
        ]
        shape = f'<polygon points="{" ".join(points)}" '
    else:  # rectangle
        shape = f'<rect x="{cx}" y="{cy}" width="{shape_size}" height="{shape_size/2}" '
    
    # Apply transformations
    transform = ""
    if rotation:
        center_x = cx + shape_size/2
        center_y = cy + shape_size/2
        transform = f'transform="rotate({rotation} {center_x} {center_y})" '
    
    # Set colors based on description
    if "light" in color.lower():
        fill_color = {
            "light red": "#ffcccc",
            "light cyan": "#ccffff",
            "light blue": "#ccddff",
            "light green": "#ccffcc",
            "light yellow": "#ffffcc",
            "light orange": "#ffe5cc",
            "light purple": "#e5ccff",
            "light pink": "#ffccdd"
        }.get(color.lower(), "#f0f0f0")
    else:
        fill_color = color.lower()
    
    stroke_color = {
        "red": "#cc0000",
        "cyan": "#00cccc", 
        "blue": "#0066cc",
        "green": "#00cc00",
        "yellow": "#cccc00",
        "orange": "#ff9900",
        "purple": "#9900cc",
        "pink": "#ff66cc"
    }.get(color.split()[-1].lower(), "#333")
    
    shape += f'fill="{fill_color}" stroke="{stroke_color}" stroke-width="2" {transform}/>'
    
    return shape

def create_coordinate_plane_with_point(point_x, point_y, point_label, point_color, 
                                       max_x=20, max_y=20, other_points=None, show_line=False):
    """Create a coordinate plane with labeled points"""
    unit_size = 25
    width = (max_x + 1) * unit_size  
    height = (max_y + 1) * unit_size
    
    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px;">
    <!-- Grid -->
    <defs>
        <pattern id="grid" width="{unit_size}" height="{unit_size}" patternUnits="userSpaceOnUse">
            <path d="M {unit_size} 0 L 0 0 0 {unit_size}" fill="none" stroke="#e0e0e0" stroke-width="1"/>
        </pattern>
    </defs>
    
    <rect width="{width}" height="{height}" fill="white"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    
    <!-- Axes -->
    <line x1="0" y1="{height}" x2="{width}" y2="{height}" stroke="#333" stroke-width="2"/>
    <line x1="0" y1="0" x2="0" y2="{height}" stroke="#333" stroke-width="2"/>
    
    <!-- Axis labels -->
    <text x="{width - 20}" y="{height - 5}" font-family="Arial" font-size="14" fill="#333">x</text>
    <text x="5" y="15" font-family="Arial" font-size="14" fill="#333">y</text>
    
    <!-- Grid numbers -->'''
    
    # Add x-axis numbers
    for i in range(0, max_x + 1, 2):
        svg += f'\n    <text x="{i * unit_size}" y="{height + 15}" font-family="Arial" font-size="10" fill="#666" text-anchor="middle">{i}</text>'
    
    # Add y-axis numbers (inverted because SVG y goes down)
    for i in range(0, max_y + 1, 2):
        svg += f'\n    <text x="-15" y="{height - i * unit_size + 3}" font-family="Arial" font-size="10" fill="#666" text-anchor="end">{i}</text>'
    
    # Add other points if specified (faded)
    if other_points:
        for pt in other_points:
            px = pt['x'] * unit_size
            py = height - pt['y'] * unit_size  # Invert y for SVG
            svg += f'\n    <circle cx="{px}" cy="{py}" r="4" fill="{pt["color"]}" opacity="0.3"/>'
            svg += f'\n    <text x="{px + 8}" y="{py - 8}" font-family="Arial" font-size="12" fill="#666" opacity="0.3">{pt["label"]}</text>'
    
    # Add main point
    px = point_x * unit_size
    py = height - point_y * unit_size  # Invert y for SVG
    
    # Add line to axis if specified  
    if show_line:
        if "vertical" in show_line:
            svg += f'\n    <line x1="{px}" y1="{py}" x2="{px}" y2="{height}" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>'
        elif "horizontal" in show_line:
            svg += f'\n    <line x1="{px}" y1="{py}" x2="0" y2="{py}" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>'
    
    svg += f'\n    <circle cx="{px}" cy="{py}" r="5" fill="{point_color}" stroke="#333" stroke-width="1"/>'
    svg += f'\n    <text x="{px + 8}" y="{py - 8}" font-family="Arial" font-size="14" font-weight="bold" fill="#333">{point_label}</text>'
    
    svg += '\n</svg>'
    return svg

def create_3d_cube_structure(width, height, depth, color="pink"):
    """Create a 3D rectangular prism made of cubes"""
    unit = 30
    offset_x = 15
    offset_y = 10
    
    total_width = width * unit + depth * offset_x + 100
    total_height = height * unit + depth * offset_y + 100
    
    svg = f'''<svg viewBox="0 0 {total_width} {total_height}" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px;">'''
    
    # Draw cubes layer by layer from back to front
    for d in range(depth-1, -1, -1):
        for h in range(height):
            for w in range(width):
                x = 50 + w * unit + d * offset_x
                y = 50 + (height - h - 1) * unit - d * offset_y
                
                # Determine color alternation
                if (w + h + d) % 2 == 0:
                    cube_color = "#ff99cc"  # pink
                else:
                    cube_color = "#cc99ff"  # purple
                
                # Front face
                svg += f'\n    <rect x="{x}" y="{y}" width="{unit}" height="{unit}" fill="{cube_color}" stroke="#333" stroke-width="1"/>'
                
                # Top face (if visible)
                if h == height - 1:
                    points = f"{x},{y} {x+unit},{y} {x+unit+offset_x},{y-offset_y} {x+offset_x},{y-offset_y}"
                    svg += f'\n    <polygon points="{points}" fill="{cube_color}" stroke="#333" stroke-width="1" opacity="0.8"/>'
                
                # Right face (if visible)  
                if w == width - 1:
                    points = f"{x+unit},{y} {x+unit},{y+unit} {x+unit+offset_x},{y+unit-offset_y} {x+unit+offset_x},{y-offset_y}"
                    svg += f'\n    <polygon points="{points}" fill="{cube_color}" stroke="#333" stroke-width="1" opacity="0.7"/>'
    
    svg += '\n</svg>'
    return svg

def create_2d_grid(rows, cols, color="pink"):
    """Create a 2D grid of colored squares"""
    unit = 30
    width = cols * unit + 20
    height = rows * unit + 20
    
    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">'''
    
    for r in range(rows):
        for c in range(cols):
            x = 10 + c * unit
            y = 10 + r * unit
            svg += f'\n    <rect x="{x}" y="{y}" width="{unit}" height="{unit}" fill="{color}" stroke="#333" stroke-width="1"/>'
    
    svg += '\n</svg>'
    return svg

def create_trapezoid(color="red", width=200, height=100):
    """Create a trapezoid shape"""
    svg = f'''<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <polygon points="50,50 250,50 200,150 100,150" 
             fill="{color}" stroke="#333" stroke-width="2"/>
    <text x="150" y="100" font-family="Arial" font-size="14" text-anchor="middle">Trapezoid</text>
    </svg>'''
    return svg

def create_parallelogram(color="green", width=200, height=100):
    """Create a parallelogram shape"""
    svg = f'''<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <polygon points="50,50 250,50 200,150 0,150" 
             fill="{color}" stroke="#333" stroke-width="2"/>
    </svg>'''
    return svg

def create_rhombus(color="yellow", size=150):
    """Create a rhombus shape"""
    svg = f'''<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <polygon points="150,50 250,150 150,250 50,150" 
             fill="{color}" stroke="#333" stroke-width="2"/>
    </svg>'''
    return svg

def create_rectangle(color="yellow", width=200, height=100):
    """Create a rectangle shape"""
    svg = f'''<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <rect x="50" y="50" width="{width}" height="{height}" 
          fill="{color}" stroke="#333" stroke-width="2"/>
    </svg>'''
    return svg

def create_square(color="blue", size=150):
    """Create a square shape"""
    svg = f'''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <rect x="50" y="50" width="{size}" height="{size}" 
          fill="{color}" stroke="#333" stroke-width="2"/>
    </svg>'''
    return svg

def create_triangle(color="green", base=200, height=150):
    """Create a triangle shape"""
    svg = f'''<svg viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px;">
    <polygon points="150,50 50,200 250,200" 
             fill="{color}" stroke="#333" stroke-width="2"/>
    <!-- Vertices marked -->
    <circle cx="150" cy="50" r="4" fill="#333"/>
    <circle cx="50" cy="200" r="4" fill="#333"/>
    <circle cx="250" cy="200" r="4" fill="#333"/>
    </svg>'''
    return svg

def create_polygon_with_properties(shape_type, description):
    """Create polygon based on description"""
    if "trapezoid" in shape_type.lower():
        return create_trapezoid(color="#ffcccc" if "red" in description else "#ccffcc")
    elif "parallelogram" in shape_type.lower():
        return create_parallelogram(color="#ccffcc" if "green" in description else "#ccccff")
    elif "rhombus" in shape_type.lower():
        return create_rhombus(color="#ffffcc" if "yellow" in description else "#ffcccc")
    elif "rectangle" in shape_type.lower() or "rectangular" in description.lower():
        return create_rectangle(color="#ffffcc" if "yellow" in description else "#ccccff")
    elif "square" in shape_type.lower():
        return create_square(color="#ccddff" if "blue" in description else "#ccffcc")
    elif "triangle" in shape_type.lower():
        return create_triangle(color="#ccffcc" if "green" in description else "#ffcccc")
    else:
        return create_square(color="#e0e0e0")  # Default

def process_json_file(json_file, output_dir):
    """Process a JSON file and generate HTML files for visual elements"""
    json_path = Path(json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html_count = 0
    
    for question in data:
        html_content = None
        question_num = question.get('question_number', '')
        
        # Handle main image_tag
        if 'image_tag' in question and question['image_tag']:
            tag = question['image_tag']
            description = question.get('backend_description', '')
            
            # Create appropriate visual based on description
            if "coordinate plane" in description.lower():
                # Parse coordinate plane description
                import re
                points = re.findall(r'Point (\w+) is labeled.*?located at the point \((-?\d+), (-?\d+)\)', description)
                
                if points:
                    # Take first point as main, others as secondary
                    main_point = points[0]
                    other_points = []
                    for p in points[1:]:
                        color_match = re.search(f'Point {p[0]}.*?with a (\w+) dot', description)
                        color = color_match.group(1) if color_match else 'gray'
                        other_points.append({
                            'label': p[0],
                            'x': int(p[1]),
                            'y': int(p[2]),
                            'color': color
                        })
                    
                    # Get color for main point
                    color_match = re.search(f'Point {main_point[0]}.*?with a[n]? (\w+) dot', description)
                    main_color = color_match.group(1) if color_match else 'red'
                    
                    svg_content = create_coordinate_plane_with_point(
                        int(main_point[1]), int(main_point[2]),
                        main_point[0], main_color,
                        other_points=other_points
                    )
                elif "blank coordinate plane" in description.lower():
                    # Create blank coordinate plane
                    svg_content = create_coordinate_plane_with_point(0, 0, "", "transparent", show_line=False)
                else:
                    svg_content = create_coordinate_plane_with_point(5, 5, "P", "red")
                    
            elif "3d rectangular prism" in description.lower() or "cubes" in description.lower():
                # Parse 3D structure description
                import re
                dims = re.findall(r'(\d+) cubes?', description)
                if len(dims) >= 3:
                    svg_content = create_3d_cube_structure(int(dims[2]), int(dims[1]), int(dims[0]))
                else:
                    svg_content = create_3d_cube_structure(3, 2, 2)
                    
            elif any(shape in description.lower() for shape in ['trapezoid', 'parallelogram', 'rhombus', 'rectangle', 'square', 'triangle']):
                # Create shape based on description
                svg_content = create_polygon_with_properties(description, description)
                
            elif "grid" in description.lower() and any(shape in description.lower() for shape in ['square', 'hexagon', 'triangle']):
                # Create shape on grid for transformations
                svg_grid, w, h, unit = create_grid_svg()
                
                # Determine shape type and properties from description
                if "square" in description.lower():
                    shape_html = add_shape_to_grid(svg_grid, "square", 2, 2, 3, description)
                elif "hexagon" in description.lower():
                    shape_html = add_shape_to_grid(svg_grid, "hexagon", 2, 2, 3, description)
                elif "triangle" in description.lower():
                    shape_html = add_shape_to_grid(svg_grid, "triangle", 2, 2, 3, description)
                
                svg_content = svg_grid + shape_html + "\n</svg>"
            else:
                # Default grid
                svg_content = create_2d_grid(3, 3, "#ffcccc")
            
            html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{tag}</title>
    <style>
        body {{ margin: 20px; font-family: Arial, sans-serif; }}
        .item {{ display: inline-block; margin: 10px; border: 1px solid #ddd; padding: 10px; }}
    </style>
</head>
<body>
    <div class="item" label="{tag}">
        {svg_content}
    </div>
</body>
</html>'''
            
            week_num = json_path.stem.split('_')[1]
            exercise_num = json_path.stem.split('_')[2].replace('E', '')
            output_file = output_dir / f"Gr6_{week_num}_E{exercise_num} {exercise_num}_{question_num}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            html_count += 1
            
        # Handle image_choice_tags
        if 'image_choice_tags' in question and question['image_choice_tags']:
            descriptions = question.get('image_choice_tags_backend_description', [])
            main_desc = question.get('backend_description', '')
            
            all_items = []
            
            # Add main image if exists
            if 'image_tag' in question:
                all_items.append((question['image_tag'], main_desc))
            
            # Add choice images
            for i, tag in enumerate(question['image_choice_tags']):
                if i < len(descriptions):
                    all_items.append((tag, descriptions[i]))
            
            if all_items:
                html_parts = []
                for tag, desc in all_items:
                    # Similar visual creation logic as above
                    if "translated" in desc.lower() or "rotated" in desc.lower() or "reflected" in desc.lower():
                        # Create transformation visual
                        svg_content = f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><rect x="50" y="50" width="100" height="100" fill="#ffcccc" stroke="#cc0000" stroke-width="2"/><text x="100" y="100" text-anchor="middle">Transform</text></svg>'
                    else:
                        svg_content = create_2d_grid(2, 3, "#ccffcc")
                    
                    html_parts.append(f'''    <div class="item" label="{tag}">
        {svg_content}
    </div>''')
                
                html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gr6_{json_path.stem.split('_')[1]}_{question_num}_choices</title>
    <style>
        body {{ margin: 20px; font-family: Arial, sans-serif; }}
        .item {{ display: inline-block; margin: 10px; border: 1px solid #ddd; padding: 10px; }}
    </style>
</head>
<body>
{chr(10).join(html_parts)}
</body>
</html>'''
                
                week_num = json_path.stem.split('_')[1]
                exercise_num = json_path.stem.split('_')[2].replace('E', '')
                output_file = output_dir / f"Gr6_{week_num}_E{exercise_num} {exercise_num}_{question_num}_choices.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                html_count += 1
                
        # Handle solution_image_tag
        if 'solution_image_tag' in question and question['solution_image_tag']:
            solution_parts = []
            for step in question['solution_image_tag']:
                if len(step) >= 3:
                    step_num, tag, desc = step[0], step[1], step[2]
                    
                    # Create visual based on description (similar logic)
                    if "coordinate plane" in desc.lower():
                        svg_content = create_coordinate_plane_with_point(5, 5, "P", "red")
                    elif "grid" in desc.lower():
                        svg_content = create_2d_grid(2, 3, "#ffccff")
                    else:
                        svg_content = create_square("#ccddff")
                    
                    solution_parts.append(f'''    <div class="item" label="{tag}">
        {svg_content}
    </div>''')
            
            if solution_parts:
                html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gr6_{json_path.stem.split('_')[1]}_{question_num}_solution</title>
    <style>
        body {{ margin: 20px; font-family: Arial, sans-serif; }}
        .item {{ display: inline-block; margin: 10px; border: 1px solid #ddd; padding: 10px; }}
    </style>
</head>
<body>
{chr(10).join(solution_parts)}
</body>
</html>'''
                
                week_num = json_path.stem.split('_')[1]
                exercise_num = json_path.stem.split('_')[2].replace('E', '')
                output_file = output_dir / f"Gr6_{week_num}_E{exercise_num} {exercise_num}_{question_num}_solution.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                html_count += 1
    
    return html_count

# Main execution
if __name__ == "__main__":
    # List of JSON files to process
    json_files = [
        "Gr6_48_E1_variations.json",
        "Gr6_47_E3_variations.json",
        "Gr6_47_E2_variations.json", 
        "Gr6_47_E1_variations.json",
        "Gr6_46_E3_variations.json",
        "Gr6_46_E2_variations.json",
        "Gr6_46_E1_variations.json"
    ]
    
    output_dir = Path("HTML")
    output_dir.mkdir(exist_ok=True)
    
    total_html = 0
    for json_file in json_files:
        if Path(json_file).exists():
            print(f"Processing {json_file}...")
            count = process_json_file(json_file, output_dir)
            total_html += count
            print(f"  Generated {count} HTML files")
        else:
            print(f"Warning: {json_file} not found")
    
    print(f"\nTotal HTML files generated: {total_html}")