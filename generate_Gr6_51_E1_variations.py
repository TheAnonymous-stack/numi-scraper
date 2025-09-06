"""
Generate variations for Gr6_51_E1 - Sums of angles in polygons
This tag has 2 templates (1_1 and 1_2), so we need 49 more variations to reach 51 total.
"""

import json
import random
import copy

def generate_polygon_angle_variations():
    """Generate 49 variations of polygon angle sum questions."""
    
    # Load the templates
    with open('parsed_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find all templates for this tag
    tag_templates = []
    for q in templates:
        if q.get('tag') == 'Gr6_51_E1':
            tag_templates.append(q)
    
    if not tag_templates:
        print("Templates not found!")
        return
    
    print(f"Found {len(tag_templates)} templates for Gr6_51_E1")
    
    variations = []
    
    # We have 2 templates, need 49 more variations
    # Mix of two types: finding unknown angle (like template 1) and finding sum (like template 2)
    
    # Polygon data: (sides, name, triangles, sum)
    polygons = [
        (3, "triangle", 1, 180),
        (4, "quadrilateral", 2, 360),
        (5, "pentagon", 3, 540),
        (6, "hexagon", 4, 720),
        (7, "heptagon", 5, 900),
        (8, "octagon", 6, 1080),
        (9, "nonagon", 7, 1260),
        (10, "decagon", 8, 1440),
        (11, "hendecagon", 9, 1620),
        (12, "dodecagon", 10, 1800)
    ]
    
    variation_count = 0
    
    # Type 1: Find unknown angle (25 variations)
    for i in range(25):
        variation_count += 1
        
        # Randomly select a template to base on
        template = random.choice(tag_templates)
        variation = copy.deepcopy(template)
        
        # Select a polygon
        sides, poly_name, triangles, total_sum = random.choice(polygons[2:])  # Skip triangle and quadrilateral for variety
        
        # Generate random angles that sum to less than total_sum
        num_known_angles = sides - 1
        
        # Generate angles with some variation
        base_angle = total_sum // sides
        known_angles = []
        remaining_sum = total_sum
        
        for j in range(num_known_angles - 1):
            # Add some randomness to each angle
            variation_amount = random.randint(-20, 20)
            angle = base_angle + variation_amount
            # Ensure angle is reasonable (between 30 and 170 degrees)
            angle = max(30, min(170, angle))
            known_angles.append(angle)
            remaining_sum -= angle
        
        # Last known angle
        second_last = remaining_sum - random.randint(base_angle - 30, base_angle + 30)
        second_last = max(30, min(170, second_last))
        known_angles.append(second_last)
        
        # The unknown angle
        unknown_angle = total_sum - sum(known_angles)
        
        # Shuffle the known angles for variety
        random.shuffle(known_angles)
        
        # Update variation fields
        variation['question_number'] = f"1_{len(tag_templates) + variation_count}"
        
        # Choose variable name
        var_names = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q', 'r', 's', 't']
        var = random.choice(var_names)
        
        variation['question_text'] = f"What is {var}?\n{var} =___°"
        variation['image_tag'] = f"Gr6_51_1_{len(tag_templates) + variation_count}"
        
        # Create backend description
        angle_list = ", ".join([f"{angle}°" for angle in known_angles])
        variation['backend_description'] = (
            f"This image shows a {poly_name} (a {sides}-sided polygon) with "
            f"{num_known_angles} of its interior angles labeled with specific degree measures, "
            f"and one unknown angle marked with the variable {var}. "
            f"The known angles are {angle_list}. The value of angle {var} is not shown"
        )
        
        variation['correct_answers'] = [str(unknown_angle)]
        
        # Update solution
        variation['solution'] = [
            [
                "1/5",
                f"Find out how many triangles make up a {poly_name}."
            ],
            [
                "2/5",
                f"A {poly_name} is made up of {triangles} triangles, which each have 180°. Multiply."
            ],
            [
                "3/5",
                f"{triangles} $\\times$ 180° = {total_sum}°\n"
                f"The angle measures of a {poly_name} add up to {total_sum}°."
            ],
            [
                "4/5",
                f"Add up the angles you know:\n{' + '.join([str(a) + '°' for a in known_angles])} = {sum(known_angles)}°"
            ],
            [
                "5/5",
                f"Set up an equation and solve for {var}.\n"
                f"{sum(known_angles)}° + {var} = {total_sum}°\n"
                f"{var} = {total_sum}° - {sum(known_angles)}°\n"
                f"{var} = {unknown_angle}°"
            ]
        ]
        
        # Update solution image tag
        variation['solution_image_tag'] = [
            [
                "1/5",
                f"Gr6_51_1_{len(tag_templates) + variation_count}_step_1",
                f"This image shows a polygon ({poly_name}) divided into {triangles} triangular sections, "
                f"all sharing a common vertex at the bottom left corner. Straight lines are drawn from "
                f"this shared vertex to the other vertices of the {poly_name}, dividing the shape into {triangles} triangles."
            ]
        ]
        
        variations.append(variation)
    
    # Type 2: Find sum of angles (24 variations)
    for i in range(24):
        variation_count += 1
        
        # Use the second template as base
        template = tag_templates[1] if len(tag_templates) > 1 else tag_templates[0]
        variation = copy.deepcopy(template)
        
        # Select a polygon
        sides, poly_name, triangles, total_sum = random.choice(polygons)
        
        # Update variation fields
        variation['question_number'] = f"1_{len(tag_templates) + variation_count}"
        variation['question_text'] = "What is the sum of the angle measures in this shape?\n___°"
        variation['image_tag'] = f"Gr6_51_1_{len(tag_templates) + variation_count}"
        
        # Create backend description with color variety
        colors = ["dark blue", "orange", "green", "purple", "red", "black", "brown", "teal"]
        color = random.choice(colors)
        
        variation['backend_description'] = (
            f"This image shows a {poly_name} (a {sides}-sided polygon) with its interior angles not labeled. "
            f"The {poly_name} is a bold {color} outline."
        )
        
        variation['correct_answers'] = [str(total_sum)]
        
        # Update solution
        if sides == 3:
            variation['solution'] = [
                [
                    "1/2",
                    "A triangle has 3 angles."
                ],
                [
                    "2/2",
                    "The angle measures of any triangle add up to 180°."
                ]
            ]
            # No solution image for triangle
            if 'solution_image_tag' in variation:
                del variation['solution_image_tag']
        else:
            variation['solution'] = [
                [
                    "1/4",
                    f"Find out how many triangles make up a {poly_name}."
                ],
                [
                    "2/4",
                    f"A {poly_name} is made up of {triangles} triangles, which each have 180°."
                ],
                [
                    "3/4",
                    f"Multiply.\n${triangles} \\times 180 = {total_sum}$"
                ],
                [
                    "4/4",
                    f"The angle measures of a {poly_name} add up to {total_sum}°."
                ]
            ]
            
            # Update solution image tag
            variation['solution_image_tag'] = [
                [
                    "1/4",
                    f"Gr6_51_1_{len(tag_templates) + variation_count}_step_1",
                    f"This image shows a {poly_name} divided into {triangles} triangles. "
                    f"The triangles are formed by drawing {triangles - 1} diagonal{'s' if triangles > 2 else ''} "
                    f"from the same vertex at the bottom left corner of the {poly_name}. "
                    f"These diagonals connect to non-adjacent vertices, creating {triangles} smaller triangles within the shape."
                ]
            ]
        
        variations.append(variation)
    
    # Save variations to file
    output_file = 'Gr6_51_E1_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(variations)} variations for Gr6_51_E1")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Templates: {len(tag_templates)} + Variations: {len(variations)} = Total: {len(tag_templates) + len(variations)}")

if __name__ == "__main__":
    generate_polygon_angle_variations()