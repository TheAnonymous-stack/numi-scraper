import json

# Read the JSON file
with open('Gr6_15_E5_variations.json', 'r') as f:
    data = json.load(f)

# Template for the HTML with map visualization
html_template = '''<div class="item" label="Gr6_15_E5_variations_image_tag">
<svg width="400" height="300" viewBox="0 0 400 300">
  <!-- Map showing {location1}, {location2}, and {location3} -->
  <!-- {location1} to {location2}: {distance1} km -->
  <!-- {location2} to {location3}: {distance2} km -->
  
  <!-- Connection lines (pink) -->
  <line x1="50" y1="150" x2="200" y2="100" stroke="#FF69B4" stroke-width="3"/>
  <line x1="200" y1="100" x2="350" y2="150" stroke="#FF69B4" stroke-width="3"/>
  
  <!-- Location dots (blue) -->
  <circle cx="50" cy="150" r="5" fill="#4169E1"/>
  <circle cx="200" cy="100" r="5" fill="#4169E1"/>
  <circle cx="350" cy="150" r="5" fill="#4169E1"/>
  
  <!-- Location labels -->
  <text x="50" y="175" text-anchor="middle" font-size="14" font-weight="bold">{location1}</text>
  <text x="200" y="85" text-anchor="middle" font-size="14" font-weight="bold">{location2}</text>
  <text x="350" y="175" text-anchor="middle" font-size="14" font-weight="bold">{location3}</text>
  
  <!-- Distance labels -->
  <text x="125" y="120" text-anchor="middle" font-size="12" fill="#FF1493">{distance1} km</text>
  <text x="275" y="120" text-anchor="middle" font-size="12" fill="#FF1493">{distance2} km</text>
</svg>
</div>
'''

# Process each quiz question
for quiz in data['quizzes']:
    # Parse the backend description to extract location names and distances
    desc = quiz['backend_description']
    
    # Extract locations and distances from the description
    # Example: "This image shows a map connecting three locations: Riverside, Georgetown, and Greenwood. 
    # Riverside is connected to Georgetown by a longer pink line labeled 8.4 km, 
    # and Georgetown is connected to Greenwood by a shorter pink line labeled 4.7 km."
    
    import re
    
    # Extract the three locations
    locations_match = re.search(r'three locations: ([^,]+), ([^,]+), and ([^.]+)\.', desc)
    if locations_match:
        loc1, loc2, loc3 = locations_match.groups()
    else:
        # Fallback parsing
        parts = desc.split('three locations: ')[1].split('. ')[0]
        locations = parts.replace(' and ', ', ').split(', ')
        loc1, loc2, loc3 = locations[0], locations[1], locations[2]
    
    # Extract distances
    distances = re.findall(r'(\d+\.\d+) km', desc)
    if len(distances) >= 2:
        dist1, dist2 = distances[0], distances[1]
    else:
        dist1, dist2 = "0.0", "0.0"
    
    # Generate the HTML
    html_content = html_template.format(
        location1=loc1.strip(),
        location2=loc2.strip(),
        location3=loc3.strip(),
        distance1=dist1,
        distance2=dist2
    )
    
    # Get the question number (e.g., "5_1" -> "1")
    q_num = quiz['question_number'].split('_')[1]
    
    # Write the HTML file
    filename = f"Gr6_15_E5 E5_{q_num}.html"
    with open(filename, 'w') as f:
        f.write(html_content)
    
    print(f"Generated {filename}")

print("All files generated successfully!")