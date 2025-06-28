from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import base64

from playwright.sync_api import TimeoutError
from typeChecker import check_fill_in_the_blank, check_multiple_choices
from jsonHandler import write_to_json
from typeChecker import check_fill_in_the_blank, check_multiple_choices, check_sorting_drag_and_drop, check_ordering_items, check_pattern_drag_and_drop
from extractors import extract_question_text, extract_answer_fill_in_the_blank, extract_answer_multiple_choices, \
    extract_answer_fill_in_the_blank_and_multiple_choices, extract_answer_ordering_items, \
    extract_answer_pattern_drag_and_drop, extract_answer_sorting_drag_and_drop


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

def process_visual_components(page, json):
    try:
        section = page.query_selector("div.question-component section.ixl-practice-crate")
        canvas = section.query_selector("canvas")
        svg = section.query_selector("svg")
        table = section.query_selector("table")
        if canvas:
            visual = canvas
        elif svg:
            visual = svg
        elif table:
            visual = table
        else:
            print("No visual component or visual component is neither canvas nor svg")
            return
        code = page.query_selector("nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace("\xa0", "").split(" ")[0]
        visual.screenshot(path=f"Grade7_Images/Grade7_{code.split('.')[0]}/Grade7_{code}.png")
        json["image_tag"] = f"Grade7_{code}"
    except Exception as e:
        print(f"Error occured: {e}")
        return


def scrape_question(url, json, scraped_questions):
    print(f"Scraping {url}...")
    skill = url.split("/")[-1]
    json["skills"] = skill
    
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

        extract_question_text(page, json)
        process_visual_components(page, json)
        code = page.query_selector(
            "nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace(
            "\xa0", "").split(" ")[0]
        if check_fill_in_the_blank(page):
            json["question_type"] = "Fill in the blank"
            extract_answer_fill_in_the_blank(page, json, code)
            scraped_questions.append(json)

        elif check_multiple_choices(page):
            json["question_type"] = "Multiple Choice Question with Single Answer"
            extract_answer_multiple_choices(page, json, code)
            scraped_questions.append(json)

        elif check_ordering_items(page):
            json["question_type"] = "Ordering Items"
            extract_answer_ordering_items(page, json, code)
            scraped_questions.append(json)

        elif check_pattern_drag_and_drop(page):
            json["question_type"] = "Pattern Drag and Drop"
            extract_answer_pattern_drag_and_drop(page, json, code)
            scraped_questions.append(json)
        elif check_sorting_drag_and_drop(page):
            json["question_type"] = "Sorting Items"
            code = page.query_selector(
                "nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace(
                "\xa0", "").split(" ")[0]
            extract_answer_sorting_drag_and_drop(page, json, code)
            scraped_questions.append(json)
        
        browser.close()

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

url = "https://ca.ixl.com/standards/ontario/math/grade-7"
urls = getTopicUrls(url)
urls = urls[:20]
# urls = ["https://ca.ixl.com/math/grade-7/write-equations-for-proportional-relationships-from-tables"]

scraped_questions = []

for link in urls:
    json = {}
    scrape_question(link, json, scraped_questions)
write_to_json(scraped_questions, "gr7Draft.json")