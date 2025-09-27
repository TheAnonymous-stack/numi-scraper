import json

# Fix Gr7_19_E1 to have 51 variations
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

# Remove the last quiz to have exactly 51
data['quizzes'] = data['quizzes'][:51]

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E1_variations.json - now has {len(data['quizzes'])} variations")

# Fix Gr7_19_E2 to have 51 variations
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

# Remove the last quiz to have exactly 51
data['quizzes'] = data['quizzes'][:51]

with open('Gr7_19_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E2_variations.json - now has {len(data['quizzes'])} variations")

# Fix Gr7_19_E3 to have 51 variations
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

# Remove the last quiz to have exactly 51
data['quizzes'] = data['quizzes'][:51]

with open('Gr7_19_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E3_variations.json - now has {len(data['quizzes'])} variations")