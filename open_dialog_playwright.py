import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://app.fabric.microsoft.com/home?experience=fabric-developer")
    page.locator("#email").fill('sakthivel.seeniv@tigeranalytics.com')
    page.locator("#submitBtn").click()
    page.get_by_placeholder("Password").fill("Tiger#1234")
    page.locator("input[value='Sign in']").click()
    page.locator("input[value='Yes']").click()
    page.locator("//span[text()='Workspaces']").click()
    page.locator("button[title='My workspace']").click()
    page.locator("//button[contains(@class,'import-button')]").click()
    page.locator("//button[contains(.,'Report, Paginated Report or Workbook')]").click()
    page.locator("//button[contains(.,'From this computer')]").click()
    time.sleep(10)
    page.set_input_files(
        "input[type='file']",
        r"C:\Users\sakthivel.seeniv\Downloads\Sales Dashboard Copy.pbix"
    )
    time.sleep(10)