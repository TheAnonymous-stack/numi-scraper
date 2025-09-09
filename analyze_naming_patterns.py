import json
import re
from pathlib import Path
from collections import Counter

# Get all HTML files
html_files = list(Path('HTML').glob('Gr6_*.html'))
html_stems = [f.stem for f in html_files]

# Analyze HTML naming patterns
html_patterns = Counter()
for stem in html_stems:
    # Try to extract pattern
    if '_E' in stem:
        # Format like Gr6_XX_EY_...
        parts = stem.split('_')
        if len(parts) >= 4:
            pattern = f"Gr6_XX_EY_{parts[3][:1]}..."
            html_patterns[pattern] += 1
    elif '_step_' in stem:
        # Format like Gr6_X_Y_Z_step_N
        pattern = "Gr6_X_Y_Z_step_N"
        html_patterns[pattern] += 1
    else:
        # Other format
        parts = stem.split('_')
        if len(parts) >= 4:
            pattern = f"Gr6_X_Y_Z{'_' + '_'.join(parts[4:]) if len(parts) > 4 else ''}"
            html_patterns[pattern] += 1

print("HTML File Naming Patterns:")
print("-" * 40)
for pattern, count in html_patterns.most_common(10):
    print(f"{pattern}: {count} files")

# Now check JSON tags
json_files = sorted(Path('.').glob('Gr6_*_variations.json'))
json_tags = []
json_patterns = Counter()

for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'quizzes' in data:
        for quiz in data['quizzes']:
            # Check all image tag fields
            if 'solution_image_tag' in quiz and quiz['solution_image_tag']:
                for step in quiz['solution_image_tag']:
                    if isinstance(step, list) and len(step) >= 2:
                        tag = step[1]
                        json_tags.append(tag)
                        # Analyze pattern
                        if tag.startswith('Gr5_'):
                            json_patterns['Gr5_...'] += 1
                        elif tag.startswith('Gr6_') and '_step_' in tag:
                            json_patterns['Gr6_X_Y_Z_step_N'] += 1
                        elif tag.startswith('Gr6_') and '_E' in tag:
                            json_patterns['Gr6_XX_EY_...'] += 1
                        else:
                            json_patterns['Other'] += 1

print("\n\nJSON Tag Patterns:")
print("-" * 40)
for pattern, count in json_patterns.most_common():
    print(f"{pattern}: {count} tags")

# Find exact matches
json_tag_set = set(json_tags)
html_stem_set = set(html_stems)
matches = json_tag_set & html_stem_set

print(f"\n\nExact Matches: {len(matches)} out of {len(json_tag_set)} JSON tags")

# Sample mismatches
print("\n\nSample JSON tags not found in HTML (first 10):")
missing = list(json_tag_set - html_stem_set)[:10]
for tag in missing:
    print(f"  - {tag}")

print("\n\nSample HTML files not referenced in JSON (first 10):")
extra = list(html_stem_set - json_tag_set)[:10]
for stem in extra:
    print(f"  - {stem}")

# Check if there's a systematic transformation
print("\n\nChecking for systematic differences...")
# Sample some JSON tags and see if there's a pattern
sample_json = list(json_tag_set)[:20]
for tag in sample_json:
    # Try various transformations
    possible_matches = []
    
    # Check if replacing underscores helps
    if tag.replace('_', '_E') in html_stem_set:
        possible_matches.append(tag.replace('_', '_E'))
    
    # Check if the tag exists with E inserted
    parts = tag.split('_')
    if len(parts) >= 3:
        with_e = f"{parts[0]}_{parts[1]}_E{parts[2]}_{'_'.join(parts[3:])}"
        if with_e in html_stem_set:
            possible_matches.append(with_e)
    
    if possible_matches:
        print(f"  {tag} might match: {possible_matches}")

print(f"\n\nTotal HTML files: {len(html_files)}")
print(f"Total unique JSON tags: {len(json_tag_set)}")
print(f"Matched: {len(matches)}")
print(f"JSON tags without HTML: {len(json_tag_set - html_stem_set)}")
print(f"HTML files without JSON reference: {len(html_stem_set - json_tag_set)}")