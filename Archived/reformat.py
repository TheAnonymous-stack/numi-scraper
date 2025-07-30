import json
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

with open("gr7Draft.json", "r") as f:
    new_data = json.load(f)

with open("gr7ScrapedQuestions.json", "r") as f:
    old_data = json.load(f)
data = old_data + new_data

with open("gr7ScrapedQuestions.json", "w") as f:
    json.dump(data, f, indent=2)

# with open("gr7ScrapedQuestionsDraft.json", "r") as f:
#     data = json.load(f)
#     for question in data:
#         url = "https://ca.ixl.com/math/grade-7/" + question["skills"]
#         if "tag" not in question:
#             with sync_playwright() as p:
#                 browser = p.chromium.launch(headless=True)  # Set to True if you don't need to see the browser
#                 page = browser.new_page()
#                 page.goto(url)
#                 try:
#                     page.wait_for_selector("button.explore-btn", timeout=3000)
#                     page.click("button.explore-btn")
#                     print("Ad closed via 'explore-btn'")
#                     code = page.query_selector(
#                         "nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace(
#                         "\xa0", "").split(" ")[0]
#                     question["tag"] = f'Gr7_{code}'
#                 except:
#                     print("No ad found or already dismissed.")
#         with open("gr7ScrapedQuestions.json", "r") as fi:
#             old_data = json.load(fi)
#         data = old_data + [question]
#         with open("gr7ScrapedQuestions.json", "w") as fii:
#             json.dump(data, fii, indent=2)



# with open("gr7ScrapedQuestions.json", "w") as f:
#     json.dump(data, f, indent=2)


