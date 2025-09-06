import json
import random
import copy

def load_templates():
    """Load template questions from the fixed JSON file"""
    with open('file_fixed.json', 'r') as f:
        data = json.load(f)
    return [q for q in data if q.get('tag') == 'Gr6_48_E2']

def generate_coordinate_variations():
    """Generate diverse coordinate transformations for translations"""
    variations = []
    
    # Different starting points across all quadrants
    start_points = [
        (-4, -2), (-3, -5), (-5, -1), (-2, -4), (-6, -3),  # Quadrant III
        (2, -3), (4, -5), (3, -2), (5, -4), (1, -6),        # Quadrant IV
        (3, 4), (2, 5), (4, 3), (5, 2), (1, 6),             # Quadrant I
        (-3, 4), (-5, 2), (-2, 5), (-4, 3), (-6, 1),       # Quadrant II
        (0, -3), (0, 4), (-3, 0), (4, 0),                   # On axes
        (-1, -1), (1, 1), (-2, 2), (2, -2)                  # Near origin
    ]
    
    # Different translation amounts (up, down, left, right)
    translations = [
        ('up', 5), ('up', 3), ('up', 4), ('up', 6), ('up', 2),
        ('down', 5), ('down', 3), ('down', 4), ('down', 6), ('down', 2),
        ('left', 5), ('left', 3), ('left', 4), ('left', 6), ('left', 2),
        ('right', 5), ('right', 3), ('right', 4), ('right', 6), ('right', 2)
    ]
    
    # Generate combinations
    used_combinations = set()
    for start in start_points:
        for direction, amount in translations:
            combo = (start, direction, amount)
            if combo not in used_combinations and len(variations) < 50:
                used_combinations.add(combo)
                
                # Calculate result
                x, y = start
                if direction == 'up':
                    result = (x, y + amount)
                    description = f"{amount} units up"
                elif direction == 'down':
                    result = (x, y - amount)
                    description = f"{amount} units down"
                elif direction == 'left':
                    result = (x - amount, y)
                    description = f"{amount} units left"
                else:  # right
                    result = (x + amount, y)
                    description = f"{amount} units right"
                
                # Ensure result is within grid bounds (-6 to 6)
                if -6 <= result[0] <= 6 and -6 <= result[1] <= 6:
                    variations.append({
                        'start': start,
                        'direction': direction,
                        'amount': amount,
                        'result': result,
                        'description': description
                    })
    
    return variations[:50]  # Return exactly 50 variations

def create_variation(template, variation_data, variation_num):
    """Create a single variation from template and variation data"""
    new_q = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    new_q['question_number'] = f"{template_num}_{variation_num}"
    
    # Update question text
    start_x, start_y = variation_data['start']
    point_name = random.choice(['A', 'B', 'C', 'D', 'P', 'Q', 'R', 'S', 'T'])
    new_q['question_text'] = f"The point {point_name}({start_x},{start_y}) is translated {variation_data['description']}. What are the coordinates of the resulting point, \n{point_name}' = (___, ___)"
    
    # Update correct answers
    result_x, result_y = variation_data['result']
    new_q['correct_answers'] = [str(result_x), str(result_y)]
    
    # Update image tags
    new_q['image_tag'] = f"Gr6_48_2_{variation_num}"
    
    # Update backend description
    quadrant_map = {
        (True, True): "first quadrant",
        (False, True): "second quadrant",
        (False, False): "third quadrant",
        (True, False): "fourth quadrant"
    }
    
    start_quadrant = quadrant_map.get((start_x > 0, start_y > 0), "on an axis")
    new_q['backend_description'] = f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. A blue point labeled '{point_name}' is plotted at ({start_x}, {start_y}) in the {start_quadrant}."
    
    # Update solution image tags
    result_quadrant = quadrant_map.get((result_x > 0, result_y > 0), "on an axis")
    new_q['solution_image_tag'] = [
        [
            "1/3",
            f"Gr6_48_2_{variation_num}_step_1",
            f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. A blue point labeled '{point_name}' is plotted at ({start_x}, {start_y}) in the {start_quadrant}."
        ],
        [
            "2/3",
            f"Gr6_48_2_{variation_num}_step_2",
            f"The image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. A blue point labeled '{point_name}' is plotted at ({start_x}, {start_y}) in the {start_quadrant}; a purple point labeled '{point_name}'' is plotted at ({result_x}, {result_y}) in the {result_quadrant}, showing a {variation_data['description'].replace('units ', '')} movement."
        ]
    ]
    
    # Update solution text
    direction = variation_data['direction']
    amount = variation_data['amount']
    
    if direction in ['up', 'down']:
        operation = "Add" if direction == 'up' else "Subtract"
        coord_change = f"{'Add' if direction == 'up' else 'Subtract'} {amount} {'to' if direction == 'up' else 'from'} the y-coordinate"
    else:
        operation = "Subtract" if direction == 'left' else "Add"
        coord_change = f"{'Subtract' if direction == 'left' else 'Add'} {amount} {'from' if direction == 'left' else 'to'} the x-coordinate"
    
    new_q['solution'] = [
        [
            "1/3",
            f"Start with the point {point_name}({start_x},{start_y})."
        ],
        [
            "2/3",
            f"Move the point {variation_data['description']}. {coord_change} to get ({result_x},{result_y})."
        ],
        [
            "3/3",
            f"{point_name}' has coordinates ({result_x},{result_y})."
        ]
    ]
    
    return new_q

def main():
    """Generate all variations for Gr6_48_E2"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_48_E2")
        return
    
    # Use the first (and only) template
    template = templates[0]
    
    # Generate variation data
    variation_data = generate_coordinate_variations()
    
    # Create all variations
    variations = []
    for i, var_data in enumerate(variation_data, start=2):  # Start from 2 since template is 1
        variation = create_variation(template, var_data, i)
        variations.append(variation)
    
    # Save variations to JSON file
    output_file = 'Gr6_48_E2_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_48_E2")
    print(f"Saved to {output_file}")
    print(f"Total questions (including template): {len(variations) + 1}")

if __name__ == "__main__":
    main()