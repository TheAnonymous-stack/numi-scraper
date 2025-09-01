import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

# tags = []
# with open("miniMapping.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         tag, skill = row
#         if skill != "empty":
#             tags.append(tag)

# Get all HTML files in the HTML directory
grade = 7
html_files = glob.glob("HTML/*.html")
html_files.sort()

print(f"Found {len(html_files)} HTML files to process")

for html_file in html_files:
    # Extract tag info from filename for directory structure
    filename = os.path.basename(html_file)
    # Try to extract week number from filename (assuming format contains Gr8_XX)
    try:
        if f"Gr{grade}_" in filename:
            week_number = int(filename.split(f"Gr{grade}_")[1].split("_")[0])
        else:
            print("failed to extract week_number")
            week_number = 1  # Default week if pattern not found
    except:
        print("failed to extract week_number")
        week_number = 1  # Default week if extraction fails

    
    # Create directory if it doesn't exist
    save_dir = f"New_Grade{grade}_Master_Images/{week_number}"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Load the HTML file
        file_path = os.path.abspath(html_file)
        driver.get(f"file://{file_path}")
        
        # Wait for the elements to be present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item")))
        
        # Find ALL items with class="item"
        item_divs = driver.find_elements(By.CLASS_NAME, "item")
        
        for item_div in item_divs:
            # Get the label attribute
            label = item_div.get_attribute("label")
            
            # Take screenshot and save with label as filename in the appropriate directory
            screenshot_path = os.path.join(save_dir, f"{label}.png")
            item_div.screenshot(screenshot_path)
            
            print(f"✓ {html_file} -> {label}")
        
    except Exception as e:
        print(f"✗ Error processing {html_file}: {str(e)}")

# Close the driver
driver.quit()
print("\nAll screenshots captured!")