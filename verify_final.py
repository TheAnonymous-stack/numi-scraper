import glob
import re

# Get all HTML files
html_files = glob.glob('html/Gr6_*.html')
print(f"Total HTML files generated: {len(html_files)}")

# Check a sample
bad_count = 0
good_count = 0
bad_files = []

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all labels
    labels = re.findall(r'label="([^"]*)"', content)
    
    # Check if any label is a placeholder
    has_placeholder = False
    for label in labels:
        if 'variations' in label or re.match(r'.*_tag_\d+$', label):
            has_placeholder = True
            break
    
    if has_placeholder:
        bad_count += 1
        bad_files.append(html_file)
    else:
        good_count += 1

print(f"\nVerification Results:")
print(f"  Files with correct labels: {good_count}")
print(f"  Files with placeholder labels: {bad_count}")

if bad_count == 0:
    print("\n✅ SUCCESS: All HTML files have proper label attributes!")
    print("\nExample label patterns found:")
    # Show some examples
    sample_file = html_files[0] if html_files else None
    if sample_file:
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        labels = re.findall(r'label="([^"]*)"', content)[:3]
        for label in labels:
            print(f"  - {label}")
else:
    print(f"\n⚠️ WARNING: {bad_count} files still have placeholder labels")
    print("First few problematic files:")
    for bad_file in bad_files[:5]:
        print(f"  - {bad_file}")