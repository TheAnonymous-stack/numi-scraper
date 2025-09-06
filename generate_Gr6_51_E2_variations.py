"""
Generate variations for Gr6_51_E2 - Exterior angles of polygons
This tag has 1 template, so we need 50 more variations to reach 51 total.
"""

import json
import random
import copy

def generate_exterior_angle_variations():
    """Generate 50 variations of exterior angle questions."""
    
    # Load the templates
    with open('parsed_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find the template for this tag
    template = None
    for q in templates:
        if q.get('tag') == 'Gr6_51_E2':
            template = q
            break
    
    if not template:
        print("Template not found!")
        return
    
    variations = []
    
    # Polygon types with pop culture themes
    polygon_themes = [
        # Basic polygons
        ("triangle", 3, "orange", None),
        ("quadrilateral", 4, "blue", None),
        ("pentagon", 5, "green", None),
        ("hexagon", 6, "purple", None),
        ("heptagon", 7, "red", None),
        ("octagon", 8, "teal", None),
        ("nonagon", 9, "brown", None),
        ("decagon", 10, "navy", None),
        
        # Pop culture themed variations
        ("triangle", 3, "golden", "shaped like the Triforce from Zelda"),
        ("quadrilateral", 4, "crimson", "resembling a Pokéball outline"),
        ("pentagon", 5, "black", "similar to the Pentagon building"),
        ("hexagon", 6, "yellow", "like a honeycomb from Minecraft"),
        ("octagon", 8, "red", "like a stop sign"),
        ("triangle", 3, "silver", "shaped like Iron Man's arc reactor core"),
        ("quadrilateral", 4, "green", "like a Creeper face from Minecraft"),
        ("pentagon", 5, "blue", "resembling Captain America's shield outline"),
        ("hexagon", 6, "orange", "like the cells in Dragon Ball Z"),
        ("triangle", 3, "purple", "shaped like the Deathly Hallows symbol"),
        
        # Anime themes
        ("triangle", 3, "red", "like the Sharingan pattern from Naruto"),
        ("hexagon", 6, "white", "resembling a shogi piece from Shogi anime"),
        ("octagon", 8, "black", "like the Eight Trigrams from Naruto"),
        ("pentagon", 5, "gold", "shaped like a star from Sailor Moon"),
        ("quadrilateral", 4, "blue", "like the Survey Corps emblem outline"),
        
        # TV series themes
        ("triangle", 3, "red", "like the Squid Game triangle guard mask"),
        ("quadrilateral", 4, "black", "shaped like the frame of a TV screen"),
        ("hexagon", 6, "green", "like the island sections in Lost"),
        ("octagon", 8, "yellow", "resembling the Dharma Initiative logo"),
        ("pentagon", 5, "silver", "like the S.H.I.E.L.D. badge"),
        
        # Gaming themes
        ("triangle", 3, "neon blue", "like a Portal turret warning sign"),
        ("quadrilateral", 4, "pixelated green", "like a Tetris block"),
        ("hexagon", 6, "dark purple", "resembling Civilization game tiles"),
        ("octagon", 8, "metallic", "like the UFC octagon cage"),
        ("pentagon", 5, "rainbow", "shaped like a Mario star"),
        
        # More variations
        ("triangle", 3, "magenta", "like a warning symbol"),
        ("quadrilateral", 4, "cyan", "shaped like a window frame"),
        ("pentagon", 5, "amber", "like a home plate in baseball"),
        ("hexagon", 6, "coral", "resembling a beehive cell"),
        ("heptagon", 7, "indigo", "like a mystical symbol"),
        ("octagon", 8, "maroon", "shaped like a gazebo top view"),
        ("nonagon", 9, "turquoise", "like an ancient coin"),
        ("decagon", 10, "lime", "resembling a gear wheel"),
    ]
    
    # Ensure we have enough variations
    while len(polygon_themes) < 50:
        colors = ["dark blue", "bright red", "forest green", "royal purple", "sunset orange", 
                 "midnight black", "pearl white", "hot pink", "electric blue", "neon green"]
        shapes = ["triangle", "quadrilateral", "pentagon", "hexagon", "heptagon", "octagon", "nonagon", "decagon"]
        
        shape = random.choice(shapes)
        sides = [3, 4, 5, 6, 7, 8, 9, 10][shapes.index(shape)]
        color = random.choice(colors)
        
        polygon_themes.append((shape, sides, color, None))
    
    # Shuffle for variety
    random.shuffle(polygon_themes)
    
    # Generate 50 variations
    for i in range(50):
        variation = copy.deepcopy(template)
        
        poly_name, sides, color, theme = polygon_themes[i]
        
        # Update question number
        variation['question_number'] = f"2_{i + 2}"
        
        # Keep the same question format
        variation['question_text'] = (
            "The diagram shows a convex polygon.\n"
            "What is the sum of the exterior angle measures, one at each vertex, of this polygon?\n___°"
        )
        
        # Update image tag
        variation['image_tag'] = f"Gr6_51_2_{i + 2}"
        
        # Create backend description
        if theme:
            variation['backend_description'] = f"This image shows a {poly_name} outlined in {color}, {theme}."
        else:
            variation['backend_description'] = f"This image shows a {poly_name} outlined in {color}."
        
        # The answer is always 360° for convex polygons
        variation['correct_answers'] = ["360"]
        
        # Update solution with variety in explanation
        explanations = [
            f"Since this polygon is convex, the sum of its exterior angle measures, one at each vertex, is 360°. The number of sides is not relevant.",
            f"For any convex polygon, the exterior angles always sum to 360°. This {poly_name} has {sides} sides, but that doesn't affect the sum.",
            f"The sum of exterior angles is always 360° for convex polygons, regardless of the number of sides. This rule applies to this {poly_name} too.",
            f"No matter how many sides a convex polygon has, its exterior angles add up to 360°. This {poly_name} follows the same rule.",
            f"This is a convex {poly_name}. Like all convex polygons, its exterior angles sum to 360°."
        ]
        
        variation['solution'] = [
            [
                "1/2",
                "Look at this convex polygon."
            ],
            [
                "2/2",
                random.choice(explanations)
            ]
        ]
        
        # Update solution image tag
        variation['solution_image_tag'] = [
            [
                "1/2",
                f"Gr6_51_2_{i + 2}_step_1",
                variation['backend_description']
            ]
        ]
        
        variations.append(variation)
    
    # Save variations to file
    output_file = 'Gr6_51_E2_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(variations)} variations for Gr6_51_E2")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Template: 1 + Variations: {len(variations)} = Total: {1 + len(variations)}")

if __name__ == "__main__":
    generate_exterior_angle_variations()