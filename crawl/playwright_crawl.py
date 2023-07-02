from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://www.baidu.com/")
    page.screenshot(path="baidu.png")
    page.wait_for_load_state('networkidle')
    browser.close()
    print("chromium is done!")

    # for browser_type in [p.chromium, p.firefox, p.webkit]:
    #     browser = browser_type.launch(headless=False)
    #     page = browser.new_page()
    #     page.goto("https://www.baidu.com/")
    #     page.screenshot(path=f"{browser_type.name}.png")
    #     browser.close()
    #     print(f"{browser_type.name} is done!")