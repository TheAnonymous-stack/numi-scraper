import json
import glob
import os

# Get all Gr7 variation files with regular fractions
regular_fraction_files = [
    'Gr7_5_E2_variations.json',
    'Gr7_5_E3_variations.json',
    'Gr7_6_E2_variations.json',
    'Gr7_7_E3_variations.json',
    'Gr7_13_E1_variations.json',
    'Gr7_13_E2_variations.json',
    'Gr7_14_E1_variations.json',
    'Gr7_14_E2_variations.json',
    'Gr7_15_E1_variations.json',
    'Gr7_15_E2_variations.json',
    'Gr7_16_E1_variations.json',
    'Gr7_16_E2_variations.json',
    'Gr7_17_E2_variations.json',
    'Gr7_20_E1_variations.json',
    'Gr7_20_E2_variations.json',
    'Gr7_20_E3_variations.json',
    'Gr7_22_E1_variations.json',
    'Gr7_22_E3_variations.json',
    'Gr7_22_E4_variations.json',
    'Gr7_27_E3_variations.json',
    'Gr7_35_E2_variations.json',
]

print("Analyzing question types in Grade 7 fraction files...\n")

for filename in regular_fraction_files:
    if not os.path.exists(filename):
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict) and "quizzes" in data:
        questions = data["quizzes"]
    elif isinstance(data, list):
        questions = data
    else:
        continue

    if questions:
        q_type = questions[0].get("question_type", "unknown")
        print(f"{filename}: {q_type}")
