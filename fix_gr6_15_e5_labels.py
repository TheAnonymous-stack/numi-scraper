import os
import re

html_dir = "html"
files_fixed = 0
labels_added = 0

# Find all Gr6_15_E5 HTML files
pattern = r"Gr6_15_E5_\d+_\d+\.html"

for filename in os.listdir(html_dir):
    if re.match(pattern, filename):
        filepath = os.path.join(html_dir, filename)

        # Extract the full name without .html for the label
        main_label = filename.replace(".html", "")

        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Check if main label already exists
        if f'label="{main_label}"' not in content:
            # Find the container div and add the main label div after it
            # Look for the opening of the container
            container_pattern = r'(<div class="container">)'

            # Create a new div with the main label that wraps the existing content
            # First, find if there's already a visual-element div
            visual_element_pattern = r'<div class="visual-element item" label="Gr6_15_E5_variations_image_tag">'

            if visual_element_pattern in content:
                # Wrap the existing visual element with the main label
                # Find the entire visual element div
                start_idx = content.find('<div class="visual-element item" label="Gr6_15_E5_variations_image_tag">')
                if start_idx != -1:
                    # Find the matching closing div
                    # Count divs to find the right closing tag
                    div_count = 1
                    idx = start_idx + len('<div class="visual-element item" label="Gr6_15_E5_variations_image_tag">')

                    while div_count > 0 and idx < len(content):
                        if content[idx:idx+5] == '<div ':
                            div_count += 1
                            idx += 5
                        elif content[idx:idx+6] == '</div>':
                            div_count -= 1
                            if div_count == 0:
                                # Found the closing div
                                end_idx = idx + 6

                                # Extract the visual element
                                visual_element = content[start_idx:end_idx]

                                # Replace with wrapped version
                                wrapped = f'<div class="visual-element item" label="{main_label}">\n  {visual_element}\n</div>'

                                content = content[:start_idx] + wrapped + content[end_idx:]
                                labels_added += 1
                                break
                            idx += 6
                        else:
                            idx += 1
            else:
                # No existing visual element, add main label div inside container
                replacement = f'\\1\n  <div class="visual-element item" label="{main_label}">\n  </div>'
                content = re.sub(container_pattern, replacement, content, count=1)
                labels_added += 1

        # Save if modified
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_fixed += 1
            print(f"Fixed: {filename}")

print(f"\nSummary:")
print(f"Files fixed: {files_fixed}")
print(f"Labels added: {labels_added}")