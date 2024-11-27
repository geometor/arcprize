from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://google.com/')
    page.screenshot(path=f'playwright_test.png')
    browser.close()
