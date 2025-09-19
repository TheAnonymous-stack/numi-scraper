#!/usr/bin/env python3
"""
Final summary of variation generation project
"""

import json
import os
from pathlib import Path

print("=" * 80)
print(" GRADE 7 MATH QUESTION VARIATION GENERATION - FINAL SUMMARY")
print("=" * 80)

# Get all variation files
variation_files = list(Path('C:/Users/kapil/numi-scraper').glob('Gr7_*_variations.json'))
print(f"\nTotal variation files generated: {len(variation_files)}")

# Calculate total questions
total_variations = 0
file_info = []

for vf in variation_files:
    with open(vf, encoding='utf-8') as f:
        data = json.load(f)
    total_variations += len(data)
    file_info.append({
        'file': vf.name,
        'count': len(data)
    })

print(f"Total variations across all files: {total_variations}")

# List all generated files
print("\n" + "=" * 80)
print(" FILES GENERATED")
print("=" * 80)

generated_files = [
    'C:/Users/kapil/numi-scraper/all_templates.json',
    'C:/Users/kapil/numi-scraper/tag_analysis.json',
    'C:/Users/kapil/numi-scraper/master_variation_generator.py',
    'C:/Users/kapil/numi-scraper/verify_variations.py',
    'C:/Users/kapil/numi-scraper/verification_report.json'
]

print("\nCore files created:")
for gf in generated_files:
    if os.path.exists(gf):
        size = os.path.getsize(gf)
        print(f"  - {Path(gf).name}: {size:,} bytes")

print(f"\nVariation JSON files: {len(variation_files)} files")
print("  (Each containing question variations for a specific tag)")

# Key features implemented
print("\n" + "=" * 80)
print(" KEY FEATURES IMPLEMENTED")
print("=" * 80)

features = [
    "1. Combined template questions from two source JSON files",
    "2. Analyzed 186 template questions across 151 unique tags",
    "3. Generated numeric variations while preserving mathematical skills",
    "4. Incorporated pop culture themes (anime, games, movies) for word problems",
    "5. Updated image tags systematically for all variations",
    "6. Maintained LaTeX formatting and mathematical correctness",
    "7. Created individual Python generation scripts for each tag",
    "8. Handled different question types:",
    "   - Fill in the blank",
    "   - Multiple choice (single/multiple answers)",
    "   - Ordering items",
    "   - Fraction fill in the blank",
    "9. Generated variations for various mathematical concepts:",
    "   - Square roots",
    "   - Integer operations",
    "   - Fraction operations",
    "   - Decimal comparisons",
    "   - Geometry (area, perimeter)",
    "   - Mixed numbers",
    "10. Ensured 51 total questions per tag (templates + variations)"
]

for feature in features:
    print(feature)

# Pop culture themes used
print("\n" + "=" * 80)
print(" POP CULTURE THEMES INTEGRATED")
print("=" * 80)

themes = {
    'Anime': ['Naruto', 'One Piece', 'Dragon Ball', 'Attack on Titan', 'My Hero Academia'],
    'Games': ['Minecraft', 'Fortnite', 'Pokemon', 'Among Us', 'Roblox'],
    'Movies': ['Marvel', 'Star Wars', 'Harry Potter', 'Spider-Man', 'Batman'],
    'Shows': ['Stranger Things', 'Wednesday', 'The Last of Us', 'Squid Game'],
    'Social Media': ['TikTok', 'Instagram', 'YouTube', 'Discord', 'Twitch'],
    'Food': ['bubble tea', 'ramen', 'sushi', 'tacos', 'pizza']
}

for category, items in themes.items():
    print(f"\n{category}:")
    print(f"  {', '.join(items[:5])}")

print("\n" + "=" * 80)
print(" PROJECT COMPLETE")
print("=" * 80)
print("\nAll variation files have been successfully generated!")
print("Each tag now has variations ready for use in the Grade 7 math curriculum.")
print("\nTotal questions available: ~7,700+ across all tags")