from playwright.sync_api import sync_playwright

def extract_youtube_from_khan(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # set to True when running headless
        page = browser.new_page()
        page.goto(url)

        # Step 1: Handle cookie popup if present
        try:
            page.locator('button#onetrust-reject-all-handler').click(timeout=3000)
        except:
            pass

        # Step 2: Close donation banner if present
        try:
            page.locator('button[data-testid="close-donate-banner"][aria-label="close"]').click(timeout=3000)
        except:
            pass

        # Step 3: Wait for video container to load
        page.wait_for_selector('div[class*="ka-video-player-container"]', timeout=10000)
        iframe = page.locator('iframe[src*="youtube"], iframe[src*="youtu.be"]')
        if iframe.count() > 0:
            src = iframe.first.get_attribute("src")
        else:
            src = None
            
        # # Step 4: Try different approaches to find the iframe
        # # Approach 1: Direct iframe search on page
        # try:
        #     iframe = page.locator('iframe[src*="youtube"], iframe[src*="youtu.be"]')
        #     if iframe.count() > 0:
        #         src = iframe.first.get_attribute("src")
        #         print(f"Found YouTube iframe directly: {src}")
        #         browser.close()
        #         return src
        # except:
        #     pass
        
        # # Approach 2: Look for iframe anywhere in the video container area
        # try:
        #     video_container = page.locator('div[class*="ka-video-player-container"]')
        #     print(f"Video container found: {video_container.count()} elements")
            
        #     # Check inner HTML to see what's there
        #     if video_container.count() > 0:
        #         inner_html = video_container.first.inner_html()
        #         print(f"Container HTML length: {len(inner_html)} chars")
        #         if "iframe" in inner_html.lower():
        #             print("iframe tag found in HTML")
        #         else:
        #             print("No iframe tag in container HTML")
            
        #     # Try to find iframe within container
        #     iframe = video_container.locator('iframe').first
        #     src = iframe.get_attribute("src", timeout=5000)
        #     print(f"Found iframe in container: {src}")
        # except Exception as e:
        #     print(f"Error finding iframe: {e}")
        #     src = None

        browser.close()
        return str(src) if src else ""