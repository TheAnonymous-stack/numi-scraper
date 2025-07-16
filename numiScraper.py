from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import base64
import re

from playwright.sync_api import TimeoutError
from typeChecker import check_fill_in_the_blank, check_multiple_choices
from jsonHandler import write_to_json

from typeChecker import check_fill_in_the_blank, check_multiple_choices, check_drag_and_drop, check_ordering_items
from extractors import extract_question_text, extract_answer_fill_in_the_blank, extract_answer_multiple_choices, extract_answer_drag_and_drop, extract_answer_ordering_items, extract_answer_pattern_drag_and_drop


def screenshot_question_section(url, output_path="question.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        counter = 1
        page = browser.new_page()    
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Attempt to close the ad using the 'explore-btn' button
            try:
                page.wait_for_selector("button.explore-btn", timeout=3000)
                page.click("button.explore-btn")
                print("Ad closed via 'explore-btn'")
            except:
                print("No ad found or already dismissed.")

            # Screenshot the question section
            section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)
            section.screenshot(path=output_path)
        except:
            print(f"question{counter-1} failed")
        print(f"Screenshots saved to {output_path}")

        browser.close()

def extract_question_text2(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        try:
            page.wait_for_selector("button.explore-btn", timeout=3000)
            page.click("button.explore-btn")
        except:
            pass

        # Wait for question section
        section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)
        text = section.inner_text().replace("\xa0", "")
        
        # Extract text
        dict = {}
        dict["question"] = text
        print(dict)
        print(text)
        browser.close()
        return text

def process_visual_components(page, json, code):
    section = page.query_selector("section.ixl-practice-crate")
    lst = code.split(".")
    base_code = lst[0] + "." + lst[1]
    try:
        
        table = section.query_selector("table")
        if table:
            table.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"

        canvas = section.query_selector("canvas")
        if canvas:

            
            canvas.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"
        
        # svgs = section.query_selector_all("svg")
        # if len(svgs) > 0:
        #     for svg in enumerate(svgs):
        #         svg.screenshot(path=f"Grade4_Images/Grade4_{code.split('.')[0]}/Grade4_{code}_{i}")
        #         i += 1
        diagramWrapper = section.query_selector("div.diagramWrapper")
        if diagramWrapper:
            diagramWrapper.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"

        fractionBar = section.query_selector("div.fractionBarBlockTable")
        if fractionBar:
            fractionBar.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"

        selectableGridContainer = section.query_selector("div.selectableGridContainer")
        if selectableGridContainer:
            selectableGridContainer.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"

        stripContainer = section.query_selector("div.has-two-bars")
        if stripContainer:
            
            stripContainer.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"
        
        multiplicationModelContainer = section.query_selector("div.multiplication-model-container")
        if multiplicationModelContainer:
            
            multiplicationModelContainer.screenshot(path=f"Grade5_Master_Images/Grade5_{code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
            
            json["image_tag"] = f"Grade5_{code}"
            

    except Exception as e:
        print(f"Error occured: {e}")
        return

def check_duplicate(questions, text):
    for question in questions:
        length = min(len(question), len(text))
        difference_count = 0
        for i in range(length):
            if question[i] != text[i]:
                difference_count += 1
        if difference_count < int(0.5 * length):
            return True
    return False
def scrape_question(url, json, scraped_questions):

        print(f"Scraping {url}...")
        skill = url.split("/")[-1]
        tracker = {
            "Fill in the blank" :[],
            "Multiple Choice": [],
            "Ordering Items": []
        }
        question_count = 0
        for _ in range(10):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)  # Set to True if you don't need to see the browser
                page = browser.new_page()
                page.goto(url)
                try:
                    page.wait_for_selector("button.explore-btn", timeout=3000)
                    page.click("button.explore-btn")
                    print("Ad closed via 'explore-btn'")
                except:
                    print("No ad found or already dismissed.")
                base_code = page.query_selector(
                                "nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace(
                                "\xa0", "").split(" ")[0]
                extract_question_text(page, json)
                text = re.split(r"\n+", json["question_text"])[0]
                if len(text) == 0:
                    json = {}
                    page.reload()
                    continue
                
                json["skills"] = skill
                section = page.query_selector("section.ixl-practice-crate")
                if check_fill_in_the_blank(page):
                    if not check_duplicate(tracker["Fill in the blank"], text):
                        question_count += 1
                        code = base_code + "." + str(question_count)
                        tracker["Fill in the blank"].append(text)
                        section.screenshot(path=f"Grade5_Questions/Grade5_{base_code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
                        process_visual_components(page, json, code)
                        tracker["Fill in the blank"].append(text)
                        json["question_type"] = "Fill in the blank"
                        json["question_number"] = code
                        json["tag"] = base_code
                        extract_answer_fill_in_the_blank(page, json, code)
                        scraped_questions.append(json)

                elif check_multiple_choices(page):
                    if not check_duplicate(tracker["Multiple Choice"], text):
                        question_count += 1
                        code = base_code + "." + str(question_count)
                        tracker["Multiple Choice"].append(text)
                        section.screenshot(path=f"Grade5_Questions/Grade5_{base_code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
                        process_visual_components(page, json, code)
                        json["question_type"] = "Multiple Choice Question with Single Answer"
                        json["question_number"] = code
                        json["tag"] = base_code
                        extract_answer_multiple_choices(page, json, code)
                        scraped_questions.append(json)
                else:
                    browser.close()
                    break
                

                # elif check_ordering_items(page):
                #     if not check_duplicate(tracker["Ordering Items"], text):
                #         tracker["Ordering Items"].append(text)
                #         section.screenshot(path=f"Grade5_Questions/Grade_{base_code.split('.')[0]}/Grade5_{base_code}/Grade5_{code}.png")
                #         process_visual_components(page, json, code)
                #         json["tag"] = code
                #         json["question_type"] = "Ordering Items"
                #         extract_answer_ordering_items(page, json, code)
                #         scraped_questions.append(json)
                    
                json = {}
                browser.close()

        # elif check_pattern_drag_and_drop(page):
        #     json["question_type"] = "Pattern Drag and Drop"
        #     json["tag"] = code
        #     extract_answer_pattern_drag_and_drop(page, json, code)
        #     scraped_questions.append(json)
        # elif check_drag_and_drop(page):
        #     json["question_type"] = "Drag and Drop"
        #     code = page.query_selector(
        #         "nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace(
        #         "\xa0", "").split(" ")[0]
        #     extract_answer_drag_and_drop(page, json, code)
        #     scraped_questions.append(json)

        

def getTopicUrls(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")

        # Find the main section with class="skill-tree-body"
        skill_tree_body = soup.find("div", id="dv-listing-standards-alignment")
        if not skill_tree_body:
            print("❌ 'skill-tree-body' section not found.")
            return []
        results = []
        categories = skill_tree_body.find_all("li", class_="each-alignment")
        base_url = "https://ca.ixl.com"
        for category in categories:
            link = base_url+category.find("a", class_="skillLink").get("href")
            results.append(link)
        return results

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return []


urls = getTopicUrls("https://ca.ixl.com/standards/ontario/math/grade-5")[175:]


scraped_questions = []
for url in urls:
    scrape_question(url, {}, scraped_questions)
write_to_json(scraped_questions, "gr5Draft.json")
# urls = getTopicUrls(url)[100:200]

# scraped_questions = []


# for link in urls:
#     json = {}
#     scrape_question(link, json, scraped_questions)
# write_to_json(scraped_questions, "gr4Draft.json")

