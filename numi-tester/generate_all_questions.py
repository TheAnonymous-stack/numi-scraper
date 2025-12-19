import json
import os

quizzes = []
html_files = []

# Template 1: Perimeter + one side → area (Questions 1-13)
config_t1 = [
    (18, 6), (20, 7), (22, 8), (24, 9), (26, 10), (28, 11), (30, 12),
    (32, 13), (34, 14), (36, 15), (40, 16), (44, 17), (48, 19)
]

for i, (perim, long) in enumerate(config_t1, 1):
    short = perim // 2 - long
    area = long * short
    quizzes.append({
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
    })

# Template 2: Consecutive sides (Questions 14-25)
perimeters_t2 = [26, 30, 34, 38, 42, 46, 50, 22, 18, 14, 10, 6]

for i, perim in enumerate(perimeters_t2, 14):
    n = (perim - 2) // 4
    area = n * (n + 1)
    quizzes.append({
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
            ["5/11", f"Since shorter side = n and longer side = n + 1 (from step 2), we can plug it in to get: 2(n) + 2(n+1) = {perim}"],
            ["6/11", f"Simplify: 2n + 2n + 2 = {perim}"],
            ["7/11", f"4n + 2 = {perim}"],
            ["8/11", f"4n = {perim - 2}"],
            ["9/11", f"n = {perim - 2} ÷ 4"],
            ["10/11", f"n = {n}. The short side is n = {n}cm and the long side is n + 1 = {n} + 1 = {n+1}cm"],
            ["11/11", f"Find the area: Area means how much space is inside the rectangle. Area = long side x short side = {n} x {n+1} = {area}"]
        ],
        "solution_image_tag": []
    })

# Template 3: Perimeter → MAX area (Questions 26-38) - NEEDS TABLES
perimeters_t3 = [20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 16, 18]

for i, perim in enumerate(perimeters_t3, 26):
    half_p = perim // 2
    max_area = (half_p // 2) ** 2 if perim % 4 == 0 else (half_p // 2) * (half_p // 2 + 1)

    quizzes.append({
        "skills": "rectangle-perimeter-to-area",
        "question_text": f"The side lengths of a rectangle with a perimeter of {perim} cm are natural numbers. Find the maximum area this rectangle can have.\n____ $\\text{{cm}}^2$",
        "tag": "Gr56_2_1",
        "correct_answers": [str(max_area)],
        "question_number": f"1_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/3", f"Identify what we know:\n• Perimeter (distance around the rectangle) = {perim}cm\n• Both sides must be natural numbers (whole numbers like 1, 2, 3, 4…)\n• We need to find: The LARGEST possible area"],
            ["2/3", f"Find all possible combinations: If a perimeter = {perim}cm, then 2 long side + 2 short side = {perim}. Dividing 2 on both sides, we get 1 long side + 1 short side = {half_p}. Let's list all possibilities where long side + short side = {half_p}:"],
            ["3/3", f"Find the maximum: Looking at our table, the largest area is {max_area}cm² when the rectangle is as close to a square as possible. Key: For a fixed perimeter, a rectangle has the largest area when it's as close to a square as possible!"]
        ],
        "solution_image_tag": [
            ["2/3", f"Gr56_1_{i}_step_3", f"This table shows all possible combinations of long side and short side that add up to {half_p} (since perimeter ÷ 2 = {half_p}). Each row shows: long side, short side, and the resulting area (long side × short side). The highlighted row shows the maximum area of {max_area}cm²."]
        ]
    })
    html_files.append((f"Gr56_1_{i}_step_3", perim, "max_area"))

# Template 4: Perimeter → MIN area (Questions 39-50) - NEEDS TABLES
perimeters_t4 = [20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 16]

for i, perim in enumerate(perimeters_t4, 39):
    half_p = perim // 2
    min_area = 1 * (half_p - 1)

    quizzes.append({
        "skills": "rectangle-perimeter-to-area",
        "question_text": f"The side lengths of a rectangle with a perimeter of {perim} cm are natural numbers. What is the minimum area of this rectangle in square centimeters?\n____ $\\text{{cm}}^2$",
        "tag": "Gr56_2_1",
        "correct_answers": [str(min_area)],
        "question_number": f"1_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/3", f"Identify what we know:\n• Perimeter (distance around the rectangle) = {perim}cm\n• Both sides must be natural numbers (whole numbers like 1, 2, 3, 4…)\n• We need to find: The SMALLEST possible area"],
            ["2/3", f"Find all possible combinations: If a perimeter = {perim}cm, then 2 long side + 2 short side = {perim}. Dividing 2 on both sides, we get 1 long side + 1 short side = {half_p}. Let's list all possibilities where long side + short side = {half_p}:"],
            ["3/3", f"Find the minimum: Looking at our table, the smallest area is {min_area}cm² when the rectangle is {half_p-1}cm x 1cm. Key: For a fixed perimeter, a rectangle has the smallest area when the sides are as different as possible (one very long, one very short)!"]
        ],
        "solution_image_tag": [
            ["2/3", f"Gr56_1_{i}_step_3", f"This table shows all possible combinations of long side and short side that add up to {half_p} (since perimeter ÷ 2 = {half_p}). Each row shows: long side, short side, and the resulting area (long side × short side). The highlighted row shows the minimum area of {min_area}cm²."]
        ]
    })
    html_files.append((f"Gr56_1_{i}_step_3", perim, "min_area"))

print(f"Exercise 1 complete: {len(quizzes)} questions")

# EXERCISE 2 STARTS HERE

# Template 5: Area + context → perimeter (Questions 1-13) - NEEDS TABLES
areas_t5 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42, 54]
contexts = [
    ("12", "2"), ("15", "2"), ("18", "2"), ("20", "2"), ("24", "2"),
    ("30", "2"), ("36", "2"), ("10", "2"), ("9", "2"), ("14", "2"),
    ("16", "2"), ("21", "2"), ("27", "2")
]

for i, (area, (first_l, first_s)) in enumerate(zip(areas_t5, contexts), 1):
    # Find factor pair closest to each other
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    closest = min(factors, key=lambda x: abs(x[0] - x[1]))
    perim = 2 * (closest[0] + closest[1])

    quizzes.append({
        "skills": "rectangle-area-to-perimeter",
        "question_text": f"Two different rectangles have areas of {area} $\\text{{cm}}^2$. One rectangle has side lengths of {first_l} cm and {first_s} cm.\n\nIf the other rectangle's side lengths are the closest natural numbers to each other, what is the perimeter of this rectangle in cm?\n\n____ cm",
        "tag": "Gr56_2_1",
        "correct_answers": [str(perim)],
        "question_number": f"2_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/2", f"Identify what we know:\n• Both rectangles have area = {area}cm²\n• First rectangle: {first_l}cm x {first_s}cm = {area}cm²\n• Second rectangle: sides are natural numbers that are closest to each other\n• We need to find: Perimeter of the second rectangle"],
            ["2/2", f"Find the perimeter: Looking at our table, the rectangle with sides closest to each other is {closest[1]}cm x {closest[0]}cm. Perimeter = 2 long side + 2 short side = 2({closest[1]}) + 2({closest[0]}) = {2*closest[1]} + {2*closest[0]} = {perim}cm"]
        ],
        "solution_image_tag": [
            ["1/2", f"Gr56_2_{i}_step_2", f"This table shows all possible factor pairs for area = {area}cm². Each row shows: long side, short side, area (long side × short side), and the difference between sides. The highlighted row shows that {closest[1]}cm × {closest[0]}cm has the smallest difference, making these the closest natural numbers to each other."]
        ]
    })
    html_files.append((f"Gr56_2_{i}_step_2", area, "closest", closest))

# Template 6: Area → count rectangles (Questions 14-25) - NEEDS TABLES
areas_t6 = [25, 49, 16, 36, 64, 81, 100, 12, 18, 20, 28, 32]

for i, area in enumerate(areas_t6, 14):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    count = len(factors)

    quizzes.append({
        "skills": "rectangle-area-to-perimeter",
        "question_text": f"How many different rectangles can be drawn with an area of {area} $\\text{{cm}}^2$ and side lengths that are natural numbers?\n\n____ rectangles",
        "tag": "Gr56_2_1",
        "correct_answers": [str(count)],
        "question_number": f"2_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/3", f"Identify what we know:\n• Area = {area}cm²\n• Both sides must be natural numbers (whole numbers like 1, 2, 3, 4...)\n• We need to find: How many DIFFERENT rectangles"],
            ["2/3", f"We have {count} different rectangles with area {area}cm²"],
            ["3/3", "Note: We count 25 × 1 and 1 × 25 as the SAME rectangle (just rotated), so we only count it once!"]
        ],
        "solution_image_tag": [
            ["1/3", f"Gr56_2_{i}_step_2", f"This table shows all factor pairs that multiply to {area}. Each row shows: long side, short side, and area (long side × short side). There are {count} possible factor pairs."]
        ]
    })
    html_files.append((f"Gr56_2_{i}_step_2", area, "count", count))

# Template 7: Area → MAX perimeter (Questions 26-38) - NEEDS TABLES
areas_t7 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42, 54]

for i, area in enumerate(areas_t7, 26):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    max_pair = max(factors, key=lambda x: 2*(x[0] + x[1]))
    max_perim = 2 * (max_pair[0] + max_pair[1])

    quizzes.append({
        "skills": "rectangle-area-to-perimeter",
        "question_text": f"Among rectangles with an area of {area} $\\text{{cm}}^2$ and side lengths that are natural numbers, what is the perimeter in cm of the rectangle with the largest perimeter?\n\n____ cm",
        "tag": "Gr56_2_1",
        "correct_answers": [str(max_perim)],
        "question_number": f"2_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/2", f"Identify what we know:\n• Area = {area}cm²\n• Both sides must be natural numbers\n• We need to find: The LARGEST perimeter"],
            ["2/2", f"Find the max perimeter: Looking at our table, the largest perimeter is {max_perim} cm when the sides are {area} cm × 1 cm. Key: For a fixed area, a rectangle has the largest perimeter when the sides are as different as possible (one very long, one very short)!"]
        ],
        "solution_image_tag": [
            ["1/2", f"Gr56_2_{i}_step_2", f"This table shows all factor pairs that multiply to {area}. Each row shows: long side, short side, area, and the calculated perimeter [2(long side) + 2(short side)]. The highlighted row shows that {area}cm × 1cm produces the maximum perimeter of {max_perim} cm."]
        ]
    })
    html_files.append((f"Gr56_2_{i}_step_2", area, "max_perim", max_pair))

# Template 8: Area → MIN perimeter (Questions 39-50) - NEEDS TABLES
areas_t8 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42]

for i, area in enumerate(areas_t8, 39):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    min_pair = min(factors, key=lambda x: 2*(x[0] + x[1]))
    min_perim = 2 * (min_pair[0] + min_pair[1])

    quizzes.append({
        "skills": "rectangle-area-to-perimeter",
        "question_text": f"If a rectangle has side lengths that are natural numbers in centimeters and an area of {area} square centimeters, what is the minimum perimeter in centimeters?",
        "tag": "Gr56_2_1",
        "correct_answers": [str(min_perim)],
        "question_number": f"2_{i}",
        "question_type": "Fill in the blank",
        "solution": [
            ["1/2", f"Identify what we know:\n• Area = {area}cm²\n• Both sides must be natural numbers\n• We need to find: The SMALLEST perimeter"],
            ["2/2", f"Find the min perimeter: Looking at our table, the smallest perimeter is {min_perim} cm when the sides are {min_pair[1]} cm × {min_pair[0]} cm. Key: For a fixed area, a rectangle has the smallest perimeter when the sides are as close as possible!"]
        ],
        "solution_image_tag": [
            ["1/2", f"Gr56_2_{i}_step_2", f"This table shows all factor pairs that multiply to {area}. Each row shows: long side, short side, area, and the calculated perimeter [2(long side) + 2(short side)]. The highlighted row shows that {min_pair[1]}cm × {min_pair[0]}cm produces the minimum perimeter of {min_perim} cm."]
        ]
    })
    html_files.append((f"Gr56_2_{i}_step_2", area, "min_perim", min_pair))

print(f"Exercise 2 complete")
print(f"Total questions: {len(quizzes)}")

# Save JSON
output = {"quizzes": quizzes}
with open(r"c:\Users\kapil\Documents\numi-tester\scaled_questions.json", "w", encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSaved to scaled_questions.json")
print(f"HTML files needed: {len(html_files)}")

# Save HTML file list for reference
with open(r"c:\Users\kapil\Documents\numi-tester\html_files_needed.txt", "w") as f:
    for item in html_files:
        f.write(str(item) + "\n")

print("Done!")
