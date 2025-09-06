"""
Generate variations for Gr6_50_E2 - Measure angles on a circle
"""

import json
import random
import copy

def generate_circle_angle_variations():
    """Generate 50 variations of circle angle measurement questions."""
    
    # Load the template
    with open('parsed_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find the template for this tag
    template = None
    for q in templates:
        if q.get('tag') == 'Gr6_50_E2':
            template = q
            break
    
    if not template:
        print("Template not found!")
        return
    
    variations = []
    
    # Generate variations with different dash intervals and angles
    dash_intervals = [5, 10, 15, 20, 30, 45]  # Common angle intervals
    
    variation_count = 0
    for dash_interval in dash_intervals:
        # For each interval, generate angles that are multiples of that interval
        max_dashes = 360 // dash_interval
        
        # Select a subset of dash counts for this interval
        if dash_interval in [5, 10]:
            # For smaller intervals, use more variations
            dash_counts = list(range(1, min(max_dashes, 20)))
        else:
            # For larger intervals, use all possible
            dash_counts = list(range(1, max_dashes))
        
        random.shuffle(dash_counts)
        
        for dash_count in dash_counts[:9]:  # Take up to 9 variations per interval
            if variation_count >= 50:
                break
                
            variation = copy.deepcopy(template)
            
            # Calculate the angle
            angle = dash_count * dash_interval
            if angle >= 360:
                continue  # Skip angles >= 360
            
            variation_count += 1
            
            # Update question number
            variation['question_number'] = f"2_{variation_count + 1}"
            
            # Update question text with the dash interval
            variation['question_text'] = f"What is the measure of this angle? The dashes are {dash_interval}° apart.\n___°"
            
            # Update the correct answer
            variation['correct_answers'] = [str(angle)]
            
            # Update image tag
            variation['image_tag'] = f"Gr6_50_2_{variation_count + 1}"
            
            # Determine angle type and direction for description
            if angle <= 90:
                direction = "upward and to the right"
                angle_desc = "acute"
            elif angle <= 180:
                direction = "to the left and upward"
                angle_desc = "obtuse"
            elif angle <= 270:
                direction = "downward and to the left"
                angle_desc = "reflex"
            else:
                direction = "to the right and downward"
                angle_desc = "reflex"
            
            # Update backend description
            variation['backend_description'] = (
                f"This image shows a circular protractor with a green shaded angle. "
                f"One ray points directly to the right at 0°, and the other ray extends {direction}, "
                f"stopping at the {angle}° mark. The angle is shaded in light green, and the arc is "
                f"highlighted in dark green. The angle being shown measures {angle} degrees."
            )
            
            # Update solution with dynamic content
            solution_steps = [
                [
                    "1/4",
                    "The part of the circle inside the angle tells you the angle's measure."
                ],
                [
                    "2/4",
                    f"The angle ends on dash number {dash_count}. The dashes are {dash_interval}° apart, "
                    f"so count by {dash_interval}° {'once' if dash_count == 1 else f'{dash_count} times'}."
                ]
            ]
            
            # Add the counting sequence
            if dash_count <= 6:
                # Show full counting for small numbers
                counting_sequence = ", ".join([f"{i * dash_interval}°" for i in range(1, dash_count + 1)])
                solution_steps.append([
                    "3/4",
                    counting_sequence
                ])
            else:
                # Show abbreviated counting for larger numbers
                solution_steps.append([
                    "3/4",
                    f"{dash_interval}°, {2 * dash_interval}°, {3 * dash_interval}°, ..., {angle}°"
                ])
            
            solution_steps.append([
                "4/4",
                f"The measure of the angle is {angle}°."
            ])
            
            variation['solution'] = solution_steps
            
            variations.append(variation)
            
            if variation_count >= 50:
                break
    
    # Save variations to file
    output_file = 'Gr6_50_E2_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(variations)} variations for Gr6_50_E2")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Template: 1 + Variations: {len(variations)} = Total: {1 + len(variations)}")

if __name__ == "__main__":
    generate_circle_angle_variations()