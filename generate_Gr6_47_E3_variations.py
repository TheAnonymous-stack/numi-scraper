import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_47_E3 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_47_E3']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_47_E3."""
    templates = load_templates()
    
    # We have 1 template, need 50 more variations
    variations = []
    
    # Generate movement variations on coordinate plane
    movement_variations = []
    
    # Generate diverse movement patterns
    for i in range(50):
        # Starting coordinates (positive only for this exercise)
        start_x = random.randint(2, 15)
        start_y = random.randint(2, 15)
        
        # Generate movement instructions
        movements = []
        directions = ['left', 'right', 'up', 'down']
        
        # Create 1-3 movements
        num_movements = random.randint(1, 3)
        
        current_x = start_x
        current_y = start_y
        
        for _ in range(num_movements):
            direction = random.choice(directions)
            
            # Determine max units based on current position
            if direction == 'left':
                max_units = min(current_x - 1, 8)
                if max_units > 0:
                    units = random.randint(1, max_units)
                    movements.append(f"left {units} {'unit' if units == 1 else 'units'}")
                    current_x -= units
            elif direction == 'right':
                max_units = min(20 - current_x, 8)
                if max_units > 0:
                    units = random.randint(1, max_units)
                    movements.append(f"right {units} {'unit' if units == 1 else 'units'}")
                    current_x += units
            elif direction == 'up':
                max_units = min(20 - current_y, 8)
                if max_units > 0:
                    units = random.randint(1, max_units)
                    movements.append(f"up {units} {'unit' if units == 1 else 'units'}")
                    current_y += units
            elif direction == 'down':
                max_units = min(current_y - 1, 8)
                if max_units > 0:
                    units = random.randint(1, max_units)
                    movements.append(f"down {units} {'unit' if units == 1 else 'units'}")
                    current_y -= units
        
        # Create question text
        if len(movements) == 1:
            question_text = f"You start at ({start_x}, {start_y}). You move {movements[0]}. Where do you end?\n(__, __)"
        elif len(movements) == 2:
            question_text = f"You start at ({start_x}, {start_y}). You move {movements[0]} and then {movements[1]}. Where do you end?\n(__, __)"
        else:
            question_text = f"You start at ({start_x}, {start_y}). You move {movements[0]}, then {movements[1]}, and then {movements[2]}. Where do you end?\n(__, __)"
        
        movement_variations.append({
            "question_text": question_text,
            "start": (start_x, start_y),
            "end": (current_x, current_y),
            "movements": movements,
            "correct_answers": [str(current_x), str(current_y)]
        })
    
    # Generate variations
    variation_num = 2  # Start from 2 since template is 1
    
    for var_data in movement_variations:
        template = templates[0]  # Only one template
        variation = copy.deepcopy(template)
        
        variation['question_number'] = f"3_{variation_num}"
        variation['question_text'] = var_data['question_text']
        variation['correct_answers'] = var_data['correct_answers']
        
        # Update image tag
        if 'image_tag' in variation:
            variation['image_tag'] = f"Gr6_47_3_{variation_num}"
        
        # Update backend description for blank grid
        max_x = max(var_data['start'][0], var_data['end'][0]) + 2
        max_y = max(var_data['start'][1], var_data['end'][1]) + 2
        max_x = min(max_x, 20)
        max_y = min(max_y, 20)
        
        variation['backend_description'] = (
            f"The image shows a blank coordinate plane. The x-axis is labeled 'x' and runs horizontally from 0 to {max_x}. "
            f"The y-axis is labeled 'y' and runs vertically from 0 to {max_y}. "
            f"The grid is marked with equal intervals, forming a {max_x}-by-{max_y} square grid."
        )
        
        # Update solution
        solution_steps = [
            ["1/" + str(len(var_data['movements']) + 2), f"First find the starting point, {var_data['start']}."]
        ]
        
        if len(var_data['movements']) == 1:
            solution_steps.append([
                "2/" + str(len(var_data['movements']) + 2),
                f"Now follow the path. You move {var_data['movements'][0]} to {var_data['end']}."
            ])
        else:
            path_desc = f"Now follow the path. You move {var_data['movements'][0]}"
            intermediate_x = var_data['start'][0]
            intermediate_y = var_data['start'][1]
            
            # Calculate intermediate positions
            for i, movement in enumerate(var_data['movements']):
                parts = movement.split()
                direction = parts[0]
                units = int(parts[1])
                
                if direction == 'left':
                    intermediate_x -= units
                elif direction == 'right':
                    intermediate_x += units
                elif direction == 'up':
                    intermediate_y += units
                elif direction == 'down':
                    intermediate_y -= units
                
                if i < len(var_data['movements']) - 1:
                    path_desc += f" to ({intermediate_x}, {intermediate_y}), then {var_data['movements'][i+1]}"
                else:
                    path_desc += f" to {var_data['end']}."
            
            solution_steps.append([
                "2/" + str(len(var_data['movements']) + 2),
                path_desc
            ])
        
        solution_steps.append([
            str(len(var_data['movements']) + 2) + "/" + str(len(var_data['movements']) + 2),
            f"You end at {var_data['end']}."
        ])
        
        variation['solution'] = solution_steps
        
        # Update solution image tags
        if 'solution_image_tag' in variation:
            new_tags = []
            
            # Step 1: Show starting point
            new_tags.append([
                "1/" + str(len(var_data['movements']) + 2),
                f"Gr6_47_3_{variation_num}_step_1",
                f"The image shows a coordinate plane. The x-axis is labeled 'x' and runs horizontally from 0 to {max_x}. "
                f"The y-axis is labeled 'y' and runs vertically from 0 to {max_y}. "
                f"The grid is marked with equal intervals, forming a {max_x}-by-{max_y} square grid. "
                f"A red point is plotted at the coordinates {var_data['start']}."
            ])
            
            # Step 2: Show movement path
            movement_desc = ""
            if len(var_data['movements']) == 1:
                movement = var_data['movements'][0]
                parts = movement.split()
                direction = parts[0]
                units = int(parts[1])
                
                if direction in ['left', 'right']:
                    line_type = "horizontal"
                    line_direction = "leftward" if direction == 'left' else "rightward"
                else:
                    line_type = "vertical"
                    line_direction = "upward" if direction == 'up' else "downward"
                
                movement_desc = f"A dashed red {line_type} line extends {line_direction} from the point {var_data['start']} to the point {var_data['end']}, showing a {line_type} movement of {units} {'unit' if units == 1 else 'units'} to the {direction}."
            else:
                movement_desc = f"A dashed red path shows the movement from {var_data['start']} through intermediate points to {var_data['end']}."
            
            new_tags.append([
                "2/" + str(len(var_data['movements']) + 2),
                f"Gr6_47_3_{variation_num}_step_2",
                f"The image shows a coordinate plane. The x-axis is labeled 'x' and runs horizontally from 0 to {max_x}, "
                f"while the y-axis is labeled 'y' and runs vertically from 0 to {max_y}. "
                f"The grid is marked with equal intervals, forming a {max_x}-by-{max_y} square grid. "
                f"A red point is plotted at the coordinates {var_data['start']}. {movement_desc}"
            ])
            
            variation['solution_image_tag'] = new_tags
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_47_E3_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_47_E3")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()