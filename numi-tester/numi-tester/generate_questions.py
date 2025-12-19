import json

# Generate all 100 questions for the scaled quiz

quizzes = []

# EXERCISE 1: Template 1 - Perimeter + one side → area (Questions 1-13)
perimeters_t1 = [18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 40, 44, 48]
long_sides_t1 = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19]

for i, (perim, long) in enumerate(zip(perimeters_t1, long_sides_t1), 1):
    short = perim // 2 - long
    area = long * short

    q = {
        "skills": "rectangle-perimeter-to-area",
        "question_text": f"What is the area in $\\text{{cm}}^2$ of a rectangle with a perimeter of {perim} cm and a long side of {long} cm?\n____ $\\text{{cm}}^2$",
        "tag": "Gr56_2_1",
        "correct_answers": [str(area)],
        "question_number": f"1_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/8", f"Identify what we know:\n• Perimeter (distance around the rectangle) = {perim}cm\n• Long side (length) = {long}cm\n• Short side (width) = ?\n• Area = ?"],
            ["2/8", "Find the short side (width): The perimeter formula means going all the way around the rectangle. A rectangle has 4 sides: 2 long sides and 2 short sides"],
            ["3/8", f"Since we are given perimeter is {perim}cm, 2 long sides + 2 short sides = {perim}cm"],
            ["4/8", f"Each long side is {long}cm so {long}cm + {long}cm + 2 short sides = {perim}cm"],
            ["5/8", f"Simplify we get {2*long} + 2 short side = {perim}"],
            ["6/8", f"Subtracting {2*long} on both sides, we get 2 short side = {perim - 2*long}"],
            ["7/8", f"Dividing 2 on both sides we get 1 short side = {short}cm"],
            ["8/8", f"Find the area: Area means how much space is inside the rectangle. Area = long side x short side = {long} x {short} = {area}"]
        ],
        "solution_image_tag": []
    }
    quizzes.append(q)

# EXERCISE 1: Template 2 - Consecutive sides (Questions 14-25)
perimeters_t2 = [26, 30, 34, 38, 42, 46, 50, 22, 18, 14, 10, 6]

for i, perim in enumerate(perimeters_t2, 14):
    n = (perim - 2) // 4
    area = n * (n + 1)

    q = {
        "skills": "rectangle-perimeter-to-area",
        "question_text": f"The side lengths of a rectangle with a perimeter of {perim} cm are consecutive natural numbers. Find the area of this rectangle.\n____ $\\text{{cm}}^2$",
        "tag": "Gr56_2_1",
        "correct_answers": [str(area)],
        "question_number": f"1_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/11", f"Identify what we know:\n• Perimeter (distance around the rectangle) = {perim}cm\n• The two different sides are consecutive natural numbers (like 5 and 6, or 9 and 10)\n• Area = ?"],
            ["2/11", "Let's call the shorter side = n. Then the longer side = n + 1 because they're consecutive numbers"],
            ["3/11", "Now we set up the equation. The perimeter formula means going all the way around the rectangle. A rectangle has 4 sides: 2 long sides and 2 short sides."],
            ["4/11", f"Since we are given perimeter is {perim}cm, 2 long sides + 2 short sides = {perim}cm"],
            ["5/11", "Since shorter side = n and longer side = n + 1 (from step 2), we can plug it in to get: 2(n) + 2(n+1) = " + str(perim)],
            ["6/11", f"Simplify: 2n + 2n + 2 = {perim}"],
            ["7/11", f"4n + 2 = {perim}"],
            ["8/11", f"4n = {perim - 2}"],
            ["9/11", f"n = {perim - 2} ÷ 4"],
            ["10/11", f"n = {n}. The short side is n = {n}cm and the long side is n + 1 = {n} + 1 = {n+1}cm"],
            ["11/11", f"Find the area: Area means how much space is inside the rectangle. Area = long side x short side = {n} x {n+1} = {area}"]
        ],
        "solution_image_tag": []
    }
    quizzes.append(q)

# Save to JSON
output = {"quizzes": quizzes}
with open(r"c:\Users\kapil\Documents\numi-tester\scaled_questions_partial.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(quizzes)} questions so far (Templates 1-2)")
print("Questions 1-13: Template 1 (Perimeter + one side)")
print("Questions 14-25: Template 2 (Consecutive sides)")
