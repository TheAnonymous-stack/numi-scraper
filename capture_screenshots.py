import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

# Get all HTML files matching the pattern
tag = "Gr4_6_E3"
week_number = int(tag.split("_")[1])  # Extract week number (2 in this case)
exercise_number = int(tag.split("E")[-1])  # Extract exercise number (4 in this case)
html_files = glob.glob(f"{tag} {exercise_number}_*.html")
html_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))  # Sort by number

print(f"Found {len(html_files)} HTML files to process")

# Create directory if it doesn't exist
save_dir = f"Grade4_Master_Images/{week_number}"
os.makedirs(save_dir, exist_ok=True)

for html_file in html_files:
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
            screenshot_path = os.path.join(save_dir, f"{label}")
            item_div.screenshot(screenshot_path)
            
            print(f"✓ {html_file} -> {label}")
        
    except Exception as e:
        print(f"✗ Error processing {html_file}: {str(e)}")

# Close the driver
driver.quit()
print("\nAll screenshots captured!")