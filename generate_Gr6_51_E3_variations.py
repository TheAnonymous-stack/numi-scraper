"""
Generate variations for Gr6_51_E3 - Identify complementary, supplementary, vertical, and adjacent angles
This tag has 4 templates (3_1, 3_2, 3_3, 3_4), so we need 47 more variations to reach 51 total.
"""

import json
import random
import copy

def generate_angle_relationship_variations():
    """Generate 47 variations of angle relationship questions."""
    
    # Load the templates
    with open('parsed_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find all templates for this tag
    tag_templates = []
    for q in templates:
        if q.get('tag') == 'Gr6_51_E3':
            tag_templates.append(q)
    
    if not tag_templates:
        print("Templates not found!")
        return
    
    print(f"Found {len(tag_templates)} templates for Gr6_51_E3")
    
    variations = []
    
    # Angle relationship types from templates
    relationship_types = [
        "supplementary",  # Template 3_1
        "vertical",        # Template 3_2
        "adjacent",        # Template 3_3
        "complementary"    # Template 3_4
    ]
    
    # Center point names for variety
    center_points = ['F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    
    # Ray endpoint names
    ray_points = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    variation_count = 0
    
    # Generate variations cycling through relationship types
    for i in range(47):
        variation_count += 1
        
        # Select template based on relationship type
        relationship_idx = i % 4
        relationship_type = relationship_types[relationship_idx]
        
        # Find matching template
        template_idx = relationship_idx if relationship_idx < len(tag_templates) else 0
        template = tag_templates[template_idx]
        variation = copy.deepcopy(template)
        
        # Select center point
        center = random.choice(center_points)
        
        # Select 6 different ray endpoints (excluding center)
        available_points = [p for p in ray_points if p != center]
        random.shuffle(available_points)
        points = available_points[:6]
        
        # Update question number
        variation['question_number'] = f"3_{len(tag_templates) + variation_count}"
        
        # Update image tag
        variation['image_tag'] = f"Gr6_51_3_{len(tag_templates) + variation_count}"
        
        # Create the question and solution based on relationship type
        if relationship_type == "supplementary":
            # Supplementary angles
            angle1 = f"\\angle {points[0]}{center}{points[1]}"
            correct_angle = f"\\angle {points[1]}{center}{points[3]}"
            
            variation['question_text'] = f"Which angle is supplementary to ${angle1}$?"
            
            # Generate choices with correct answer at random position
            choices = [
                f"${correct_angle}$",
                f"$\\angle {points[1]}{center}{points[2]}$",
                f"$\\angle {points[0]}{center}{points[2]}$",
                f"$\\angle {points[2]}{center}{points[4]}$"
            ]
            
            correct_idx = random.randint(0, 3)
            if correct_idx != 0:
                choices[0], choices[correct_idx] = choices[correct_idx], choices[0]
            
            variation['choices'] = choices
            variation['correct_answers'] = [chr(65 + correct_idx)]  # A, B, C, or D
            
            variation['solution'] = [
                [
                    "1/2",
                    f"Look at ${angle1}$ and ${correct_angle}$:"
                ],
                [
                    "2/2",
                    f"${correct_angle}$ is supplementary to ${angle1}$. Together they form a straight line, "
                    f"which has a measure of 180°. So, their angles add up to 180°"
                ]
            ]
            
            variation['backend_description'] = (
                f"The diagram shows six rays extending from a common central point labeled {center}. "
                f"Each ray points in a different direction and is labeled with a letter at its endpoint: "
                f"{', '.join(points)}. Among these, points {points[0]}, {center}, and {points[3]} form one straight line."
            )
            
        elif relationship_type == "vertical":
            # Vertical angles
            angle1 = f"\\angle {points[3]}{center}{points[4]}"
            correct_angle = f"\\angle {points[0]}{center}{points[1]}"
            
            variation['question_text'] = f"Which angle is vertical to ${angle1}$?"
            
            choices = [
                f"${correct_angle}$",
                f"$\\angle {points[4]}{center}{points[5]}$",
                f"$\\angle {points[4]}{center}{points[0]}$",
                f"$\\angle {points[0]}{center}{points[2]}$"
            ]
            
            correct_idx = random.randint(0, 3)
            if correct_idx != 0:
                choices[0], choices[correct_idx] = choices[correct_idx], choices[0]
            
            variation['choices'] = choices
            variation['correct_answers'] = [chr(65 + correct_idx)]
            
            variation['solution'] = [
                [
                    "1/3",
                    "Vertical angles are angles formed opposite each other when two lines intersect."
                ],
                [
                    "2/3",
                    f"Look at ${angle1}$ and ${correct_angle}$:"
                ],
                [
                    "3/3",
                    f"${correct_angle}$ and ${angle1}$ are vertical angles."
                ]
            ]
            
            variation['backend_description'] = (
                f"The diagram shows six rays extending from a central point labeled {center}. "
                f"Each ray ends at a labeled point: {', '.join(points)}. "
                f"Among them, points {points[0]}, {center}, and {points[3]} lie along the same straight line, "
                f"as do points {points[1]}, {center}, and {points[4]}."
            )
            
        elif relationship_type == "adjacent":
            # Adjacent angles
            angle1 = f"\\angle {points[4]}{center}{points[5]}"
            correct_angle = f"\\angle {points[2]}{center}{points[4]}"
            
            variation['question_text'] = f"Which angle is adjacent to ${angle1}$?"
            
            choices = [
                f"$\\angle {points[1]}{center}{points[2]}$",
                f"$\\angle {points[1]}{center}{points[3]}$",
                f"$\\angle {points[4]}{center}{points[0]}$",
                f"${correct_angle}$"
            ]
            
            correct_idx = random.randint(0, 3)
            if correct_idx != 3:
                choices[3], choices[correct_idx] = choices[correct_idx], choices[3]
            
            variation['choices'] = choices
            variation['correct_answers'] = [chr(65 + correct_idx)]
            
            variation['solution'] = [
                [
                    "1/3",
                    "Adjacent angles share a vertex and a side, but no interior points."
                ],
                [
                    "2/3",
                    f"Look at ${angle1}$ and ${correct_angle}$:"
                ],
                [
                    "3/3",
                    f"${correct_angle}$ is adjacent to ${angle1}$"
                ]
            ]
            
            variation['backend_description'] = (
                f"The diagram shows six rays extending from a central point labeled {center}, "
                f"with endpoints labeled {', '.join(points)}. All rays radiate outward from point {center} in different directions."
            )
            
        else:  # complementary
            angle1 = f"\\angle {points[0]}{center}{points[1]}"
            correct_angle = f"\\angle {points[2]}{center}{points[3]}"
            
            variation['question_text'] = f"Which angle is complementary to ${angle1}$?"
            
            choices = [
                f"$\\angle {points[1]}{center}{points[2]}$",
                f"${correct_angle}$",
                f"$\\angle {points[3]}{center}{points[4]}$",
                f"$\\angle {points[4]}{center}{points[5]}$"
            ]
            
            correct_idx = random.randint(0, 3)
            if correct_idx != 1:
                choices[1], choices[correct_idx] = choices[correct_idx], choices[1]
            
            variation['choices'] = choices
            variation['correct_answers'] = [chr(65 + correct_idx)]
            
            variation['solution'] = [
                [
                    "1/4",
                    f"Look at ${angle1}$ and ${correct_angle}$:"
                ],
                [
                    "2/4",
                    f"${correct_angle}$ is complementary to ${angle1}$.\n"
                    f"First, notice that ${angle1}$ and $\\angle {points[5]}{center}{points[0]}$ are complementary. "
                    f"Along with the right angle, they form a straight line. The straight line measures $180^\\circ$ "
                    f"and the right angle measures $90^\\circ$. That leaves another $90^\\circ$, so ${angle1}$ and "
                    f"$\\angle {points[5]}{center}{points[0]}$ have measures that add up to $90^\\circ$."
                ],
                [
                    "3/4",
                    f"Next, notice that $\\angle {points[5]}{center}{points[0]}$ and ${correct_angle}$ are vertical angles. "
                    f"That means they have the same measure."
                ],
                [
                    "4/4",
                    f"Since ${angle1}$ and $\\angle {points[5]}{center}{points[0]}$ are complementary, "
                    f"${angle1}$ and ${correct_angle}$ are also complementary. Their angles add up to $90^\\circ$."
                ]
            ]
            
            variation['backend_description'] = (
                f"The diagram shows six rays extending from a central point labeled {center}, "
                f"with endpoints labeled {', '.join(points)}. "
                f"In this image, the angle {points[4]}{center}{points[5]} is highlighted in red, "
                f"showing the angle formed between rays. The red arc indicates that it is a right angle, measuring 90°."
            )
        
        # Update solution image tags
        if relationship_type == "supplementary":
            variation['solution_image_tag'] = [
                [
                    "1/2",
                    f"Gr6_51_3_{len(tag_templates) + variation_count}_step_1",
                    f"This image shows the same diagram, but highlights the angle {angle1[7:-1]} in purple, "
                    f"and the angle {correct_angle[7:-1]} in green."
                ]
            ]
        elif relationship_type == "vertical":
            variation['solution_image_tag'] = [
                [
                    "2/3",
                    f"Gr6_51_3_{len(tag_templates) + variation_count}_step_2",
                    f"This image shows the same diagram with angles highlighted. "
                    f"The angle {angle1[7:-1]} and {correct_angle[7:-1]} are shown as vertical angles."
                ]
            ]
        elif relationship_type == "adjacent":
            variation['solution_image_tag'] = [
                [
                    "2/3",
                    f"Gr6_51_3_{len(tag_templates) + variation_count}_step_2",
                    f"This image shows the same diagram with the angle {correct_angle[7:-1]} highlighted in purple, "
                    f"and the angle {angle1[7:-1]} highlighted in blue."
                ]
            ]
        else:  # complementary
            variation['solution_image_tag'] = [
                [
                    "1/4",
                    f"Gr6_51_3_{len(tag_templates) + variation_count}_step_1",
                    f"This image shows the same diagram with the angle {angle1[7:-1]} highlighted in brown, "
                    f"and the angle {correct_angle[7:-1]} highlighted in green."
                ]
            ]
        
        variations.append(variation)
    
    # Save variations to file
    output_file = 'Gr6_51_E3_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(variations)} variations for Gr6_51_E3")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Templates: {len(tag_templates)} + Variations: {len(variations)} = Total: {len(tag_templates) + len(variations)}")

if __name__ == "__main__":
    generate_angle_relationship_variations()