import json

# Fix Gr7_19_E1 to have 51 entries
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

# Remove the last entry to have exactly 51
data['quizzes'] = data['quizzes'][:51]

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E1_variations.json - now has {len(data['quizzes'])} entries")