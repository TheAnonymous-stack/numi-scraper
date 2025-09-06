import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_46_E2 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_46_E2']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_46_E2."""
    templates = load_templates()
    
    # We have 2 templates, need 49 more variations
    variations = []
    
    # Properties of polygons variations
    polygon_properties = [
        # Template 1 variations - Every quadrilateral has ___
        {
            "question_text": "Complete the sentence.\nEvery quadrilateral has ___.",
            "choices": ["4 pairs of congruent sides", "4 vertices", "4 parallel sides", "3 angles"],
            "correct_answer": "B",
            "solution": "Every quadrilateral has 4 vertices.",
            "solution_image_desc": "This image shows a quadrilateral with 4 vertices marked with dots. The sides vary in length and the angles are different sizes."
        },
        {
            "question_text": "Complete the sentence.\nEvery quadrilateral has ___.",
            "choices": ["4 angles", "3 sides", "5 vertices", "6 edges"],
            "correct_answer": "A",
            "solution": "Every quadrilateral has 4 angles.",
            "solution_image_desc": "This image shows a quadrilateral with 4 angles marked. The angles are all different sizes."
        },
        {
            "question_text": "Complete the sentence.\nEvery triangle has ___.",
            "choices": ["4 sides", "3 vertices", "2 angles", "5 edges"],
            "correct_answer": "B",
            "solution": "Every triangle has 3 vertices.",
            "solution_image_desc": "This image shows a triangle with 3 vertices marked with dots."
        },
        {
            "question_text": "Complete the sentence.\nEvery pentagon has ___.",
            "choices": ["4 sides", "6 angles", "5 sides", "3 vertices"],
            "correct_answer": "C",
            "solution": "Every pentagon has 5 sides.",
            "solution_image_desc": "This image shows a pentagon with 5 sides. The sides may vary in length."
        },
        {
            "question_text": "Complete the sentence.\nEvery hexagon has ___.",
            "choices": ["5 vertices", "6 angles", "7 sides", "4 angles"],
            "correct_answer": "B",
            "solution": "Every hexagon has 6 angles.",
            "solution_image_desc": "This image shows a hexagon with 6 angles marked. The angles may vary in size."
        },
        {
            "question_text": "Complete the sentence.\nEvery octagon has ___.",
            "choices": ["8 vertices", "6 sides", "9 angles", "7 edges"],
            "correct_answer": "A",
            "solution": "Every octagon has 8 vertices.",
            "solution_image_desc": "This image shows an octagon with 8 vertices marked with dots."
        },
        # Template 2 variations - All ___ have specific properties
        {
            "question_text": "Complete the sentence.\nAll ___ have 4 congruent sides.",
            "choices": ["rectangles", "trapezoids", "rhombuses", "parallelograms"],
            "correct_answer": "C",
            "solution": "All rhombuses have 4 congruent sides.",
            "solution_image_desc": "This image shows a rhombus with all 4 sides marked as equal length with tick marks."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have 2 pairs of parallel sides.",
            "choices": ["trapezoids", "triangles", "parallelograms", "pentagons"],
            "correct_answer": "C",
            "solution": "All parallelograms have 2 pairs of parallel sides.",
            "solution_image_desc": "This image shows a parallelogram with parallel sides indicated by arrows."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have exactly 1 pair of parallel sides.",
            "choices": ["trapezoids", "rectangles", "squares", "rhombuses"],
            "correct_answer": "A",
            "solution": "All trapezoids have exactly 1 pair of parallel sides.",
            "solution_image_desc": "This image shows a trapezoid with one pair of parallel sides indicated by arrows."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have 4 right angles and 4 congruent sides.",
            "choices": ["rectangles", "rhombuses", "squares", "trapezoids"],
            "correct_answer": "C",
            "solution": "All squares have 4 right angles and 4 congruent sides.",
            "solution_image_desc": "This image shows a square with right angles marked and all sides equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have opposite sides that are congruent.",
            "choices": ["trapezoids", "parallelograms", "triangles", "pentagons"],
            "correct_answer": "B",
            "solution": "All parallelograms have opposite sides that are congruent.",
            "solution_image_desc": "This image shows a parallelogram with opposite sides marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have 3 sides.",
            "choices": ["quadrilaterals", "triangles", "pentagons", "hexagons"],
            "correct_answer": "B",
            "solution": "All triangles have 3 sides.",
            "solution_image_desc": "This image shows a triangle with its 3 sides highlighted."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have diagonals that bisect each other.",
            "choices": ["trapezoids", "triangles", "parallelograms", "irregular quadrilaterals"],
            "correct_answer": "C",
            "solution": "All parallelograms have diagonals that bisect each other.",
            "solution_image_desc": "This image shows a parallelogram with diagonals that intersect at their midpoints."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ are quadrilaterals.",
            "choices": ["pentagons", "squares", "triangles", "hexagons"],
            "correct_answer": "B",
            "solution": "All squares are quadrilaterals.",
            "solution_image_desc": "This image shows a square, which is a type of quadrilateral."
        },
        {
            "question_text": "Complete the sentence.\nEvery parallelogram has ___.",
            "choices": ["1 pair of parallel sides", "3 sides", "2 pairs of parallel sides", "5 angles"],
            "correct_answer": "C",
            "solution": "Every parallelogram has 2 pairs of parallel sides.",
            "solution_image_desc": "This image shows a parallelogram with both pairs of parallel sides marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery rhombus has ___.",
            "choices": ["4 congruent sides", "3 angles", "5 vertices", "6 sides"],
            "correct_answer": "A",
            "solution": "Every rhombus has 4 congruent sides.",
            "solution_image_desc": "This image shows a rhombus with all 4 sides marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have angles that add up to 180°.",
            "choices": ["quadrilaterals", "pentagons", "triangles", "hexagons"],
            "correct_answer": "C",
            "solution": "All triangles have angles that add up to 180°.",
            "solution_image_desc": "This image shows a triangle with its three angles marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have angles that add up to 360°.",
            "choices": ["triangles", "quadrilaterals", "pentagons", "hexagons"],
            "correct_answer": "B",
            "solution": "All quadrilaterals have angles that add up to 360°.",
            "solution_image_desc": "This image shows a quadrilateral with its four angles marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery square has ___.",
            "choices": ["3 right angles", "5 sides", "4 right angles", "2 parallel sides"],
            "correct_answer": "C",
            "solution": "Every square has 4 right angles.",
            "solution_image_desc": "This image shows a square with all 4 right angles marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery rectangle has ___.",
            "choices": ["4 congruent sides", "opposite sides congruent", "3 vertices", "5 angles"],
            "correct_answer": "B",
            "solution": "Every rectangle has opposite sides congruent.",
            "solution_image_desc": "This image shows a rectangle with opposite sides marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ are parallelograms.",
            "choices": ["trapezoids", "triangles", "rectangles", "pentagons"],
            "correct_answer": "C",
            "solution": "All rectangles are parallelograms.",
            "solution_image_desc": "This image shows a rectangle, which is a special type of parallelogram."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ are rectangles.",
            "choices": ["parallelograms", "squares", "rhombuses", "trapezoids"],
            "correct_answer": "B",
            "solution": "All squares are rectangles.",
            "solution_image_desc": "This image shows a square, which is a special type of rectangle."
        },
        {
            "question_text": "Complete the sentence.\nEvery trapezoid has ___.",
            "choices": ["2 pairs of parallel sides", "exactly 1 pair of parallel sides", "3 sides", "5 vertices"],
            "correct_answer": "B",
            "solution": "Every trapezoid has exactly 1 pair of parallel sides.",
            "solution_image_desc": "This image shows a trapezoid with one pair of parallel sides marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have perpendicular diagonals.",
            "choices": ["rectangles", "parallelograms", "rhombuses", "trapezoids"],
            "correct_answer": "C",
            "solution": "All rhombuses have perpendicular diagonals.",
            "solution_image_desc": "This image shows a rhombus with diagonals that meet at right angles."
        },
        {
            "question_text": "Complete the sentence.\nEvery polygon has ___.",
            "choices": ["at least 3 sides", "exactly 4 sides", "at most 2 sides", "exactly 5 vertices"],
            "correct_answer": "A",
            "solution": "Every polygon has at least 3 sides.",
            "solution_image_desc": "This image shows various polygons, all with at least 3 sides."
        }
    ]
    
    # Add more variations to reach 49 total
    additional_variations = [
        {
            "question_text": "Complete the sentence.\nAll ___ have equal diagonals.",
            "choices": ["parallelograms", "rectangles", "rhombuses", "trapezoids"],
            "correct_answer": "B",
            "solution": "All rectangles have equal diagonals.",
            "solution_image_desc": "This image shows a rectangle with diagonals of equal length marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery decagon has ___.",
            "choices": ["8 sides", "9 vertices", "10 vertices", "11 angles"],
            "correct_answer": "C",
            "solution": "Every decagon has 10 vertices.",
            "solution_image_desc": "This image shows a decagon with 10 vertices marked with dots."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ are rhombuses.",
            "choices": ["rectangles", "squares", "trapezoids", "parallelograms"],
            "correct_answer": "B",
            "solution": "All squares are rhombuses.",
            "solution_image_desc": "This image shows a square, which is a special type of rhombus."
        },
        {
            "question_text": "Complete the sentence.\nEvery regular polygon has ___.",
            "choices": ["all sides congruent", "exactly 4 sides", "at most 3 angles", "different angle measures"],
            "correct_answer": "A",
            "solution": "Every regular polygon has all sides congruent.",
            "solution_image_desc": "This image shows regular polygons with all sides marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have at least one obtuse angle.",
            "choices": ["acute triangles", "obtuse triangles", "right triangles", "equilateral triangles"],
            "correct_answer": "B",
            "solution": "All obtuse triangles have at least one obtuse angle.",
            "solution_image_desc": "This image shows an obtuse triangle with one angle greater than 90 degrees."
        },
        {
            "question_text": "Complete the sentence.\nEvery isosceles triangle has ___.",
            "choices": ["3 congruent sides", "at least 2 congruent sides", "no congruent sides", "4 sides"],
            "correct_answer": "B",
            "solution": "Every isosceles triangle has at least 2 congruent sides.",
            "solution_image_desc": "This image shows an isosceles triangle with two equal sides marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have 3 acute angles.",
            "choices": ["obtuse triangles", "right triangles", "acute triangles", "scalene triangles"],
            "correct_answer": "C",
            "solution": "All acute triangles have 3 acute angles.",
            "solution_image_desc": "This image shows an acute triangle with all three angles less than 90 degrees."
        },
        {
            "question_text": "Complete the sentence.\nEvery kite has ___.",
            "choices": ["4 congruent sides", "2 pairs of adjacent congruent sides", "no congruent sides", "3 vertices"],
            "correct_answer": "B",
            "solution": "Every kite has 2 pairs of adjacent congruent sides.",
            "solution_image_desc": "This image shows a kite with two pairs of adjacent equal sides marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have angles that add up to 540°.",
            "choices": ["quadrilaterals", "pentagons", "hexagons", "triangles"],
            "correct_answer": "B",
            "solution": "All pentagons have angles that add up to 540°.",
            "solution_image_desc": "This image shows a pentagon with its five angles marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery equilateral triangle has ___.",
            "choices": ["3 congruent angles", "2 right angles", "1 obtuse angle", "4 sides"],
            "correct_answer": "A",
            "solution": "Every equilateral triangle has 3 congruent angles.",
            "solution_image_desc": "This image shows an equilateral triangle with all three 60° angles marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have opposite angles congruent.",
            "choices": ["trapezoids", "parallelograms", "triangles", "pentagons"],
            "correct_answer": "B",
            "solution": "All parallelograms have opposite angles congruent.",
            "solution_image_desc": "This image shows a parallelogram with opposite angles marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nEvery regular hexagon has ___.",
            "choices": ["5 sides", "6 congruent sides", "7 vertices", "8 angles"],
            "correct_answer": "B",
            "solution": "Every regular hexagon has 6 congruent sides.",
            "solution_image_desc": "This image shows a regular hexagon with all 6 sides marked as equal."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have exactly one right angle.",
            "choices": ["right triangles", "rectangles", "squares", "parallelograms"],
            "correct_answer": "A",
            "solution": "All right triangles have exactly one right angle.",
            "solution_image_desc": "This image shows a right triangle with one 90° angle marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery nonagon has ___.",
            "choices": ["7 sides", "8 vertices", "9 sides", "10 angles"],
            "correct_answer": "C",
            "solution": "Every nonagon has 9 sides.",
            "solution_image_desc": "This image shows a nonagon with its 9 sides highlighted."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have angles that add up to 720°.",
            "choices": ["pentagons", "hexagons", "heptagons", "octagons"],
            "correct_answer": "B",
            "solution": "All hexagons have angles that add up to 720°.",
            "solution_image_desc": "This image shows a hexagon with its six angles marked."
        },
        {
            "question_text": "Complete the sentence.\nEvery scalene triangle has ___.",
            "choices": ["all sides different lengths", "all sides equal", "two sides equal", "four sides"],
            "correct_answer": "A",
            "solution": "Every scalene triangle has all sides different lengths.",
            "solution_image_desc": "This image shows a scalene triangle with three different side lengths."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ are convex polygons.",
            "choices": ["stars", "regular polygons", "concave polygons", "irregular shapes"],
            "correct_answer": "B",
            "solution": "All regular polygons are convex polygons.",
            "solution_image_desc": "This image shows regular polygons, all of which are convex."
        },
        {
            "question_text": "Complete the sentence.\nEvery heptagon has ___.",
            "choices": ["6 vertices", "7 angles", "8 sides", "5 diagonals"],
            "correct_answer": "B",
            "solution": "Every heptagon has 7 angles.",
            "solution_image_desc": "This image shows a heptagon with its 7 angles marked."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have no parallel sides.",
            "choices": ["trapezoids", "parallelograms", "scalene triangles", "rectangles"],
            "correct_answer": "C",
            "solution": "All scalene triangles have no parallel sides.",
            "solution_image_desc": "This image shows a scalene triangle with no parallel sides."
        },
        {
            "question_text": "Complete the sentence.\nEvery regular octagon has ___.",
            "choices": ["all angles equal", "6 sides", "9 vertices", "10 angles"],
            "correct_answer": "A",
            "solution": "Every regular octagon has all angles equal.",
            "solution_image_desc": "This image shows a regular octagon with all angles marked as 135°."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have diagonals that are perpendicular.",
            "choices": ["rectangles", "squares", "parallelograms", "trapezoids"],
            "correct_answer": "B",
            "solution": "All squares have diagonals that are perpendicular.",
            "solution_image_desc": "This image shows a square with perpendicular diagonals marked at 90°."
        },
        {
            "question_text": "Complete the sentence.\nEvery right angle measures ___.",
            "choices": ["45°", "90°", "180°", "360°"],
            "correct_answer": "B",
            "solution": "Every right angle measures 90°.",
            "solution_image_desc": "This image shows a right angle marked as 90°."
        },
        {
            "question_text": "Complete the sentence.\nAll ___ have interior angles less than 180°.",
            "choices": ["convex polygons", "concave polygons", "stars", "irregular shapes"],
            "correct_answer": "A",
            "solution": "All convex polygons have interior angles less than 180°.",
            "solution_image_desc": "This image shows convex polygons with all interior angles less than 180°."
        },
        {
            "question_text": "Complete the sentence.\nEvery dodecagon has ___.",
            "choices": ["10 sides", "11 vertices", "12 sides", "13 angles"],
            "correct_answer": "C",
            "solution": "Every dodecagon has 12 sides.",
            "solution_image_desc": "This image shows a dodecagon with its 12 sides highlighted."
        }
    ]
    
    # Combine original and additional variations
    all_variations = polygon_properties[:25] + additional_variations
    
    # Randomly select a template for each variation
    variation_num = 3  # Start from 3 since we have templates 1 and 2
    
    for var_data in all_variations:  # Generate 49 variations
        template = random.choice(templates)
        template_num = template['question_number'].split('_')[0]
        
        variation = copy.deepcopy(template)
        variation['question_number'] = f"{template_num}_{variation_num}"
        variation['question_text'] = var_data['question_text']
        variation['choices'] = var_data['choices']
        variation['correct_answers'] = [var_data['correct_answer']]
        
        # Update solution
        variation['solution'] = [
            [
                "1/1" if len(var_data.get('solution', '').split('\n')) == 1 else "1/2",
                var_data['solution']
            ]
        ]
        
        # Update solution image tag if present
        if 'solution_image_tag' in variation:
            step_num = variation['solution'][0][0]
            old_tag = variation['solution_image_tag'][0][1]
            # Update image tag with new variation number
            new_tag = old_tag.replace(f"_{template['question_number'].replace('_', '_')}_", f"_{variation['question_number'].replace('_', '_')}_")
            variation['solution_image_tag'][0][1] = new_tag
            variation['solution_image_tag'][0][2] = var_data['solution_image_desc']
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_46_E2_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_46_E2")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()