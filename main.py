import os
import time
from selenium import webdriver
from playwright.sync_api import Playwright, sync_playwright


# Set up the Playwright browser
def setup_browser() -> Playwright:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        return p, page


# Log in to YouTube using Selenium
def login(driver: webdriver.Chrome):
    driver.get("https://www.youtube.com")
    time.sleep(5) # wait for page to load
    driver.find_element_by_xpath("//yt-formatted-string[text()='Sign in']").click()
    time.sleep(5) # wait for page to load
    driver.find_element_by_name("identifier").send_keys(os.environ.get("GMAIL"))
    driver.find_element_by_id("identifierNext").click()
    time.sleep(5) # wait for page to load
    driver.find_element_by_name("password").send_keys(os.environ.get("GMAIL_PASSWORD"))
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5) # wait for page to load


# Download video from the index page using Playwright
def download_video(page):
    page.goto("https://www.youtube.com")
    time.sleep(5) # wait for page to load
    video = page.locator("//ytd-rich-item-renderer").locator("a[id='thumbnail']").locator("img")
    video_title = video.get_attribute("alt")
    video.click()
    time.sleep(10) # wait for video to load
    page.locator("button.ytp-fullscreen-button").click() # enter fullscreen
    time.sleep(5) # wait for video to load
    page.keyboard.press("d") # download video
    time.sleep(10) # wait for video to download
    return video_title


# Upload video to your YouTube channel using Selenium
def upload_video(driver: webdriver.Chrome, video_title: str):
    driver.get("https://www.youtube.com/upload")
    time.sleep(10) # wait for page to load
    driver.find_element_by_name("Filedata").send_keys(os.path.abspath("final.mp4"))
    time.sleep(10) # wait for upload to complete
    driver.find_element_by_name("title").send_keys(video_title)
    driver.find_element_by_name("privacy").click() # choose video privacy
    driver.find_element_by_xpath("//div[text()='Public']").click()
    driver.find_element_by_xpath("//span[text()='Publish']").click()
    time.sleep(10) # wait for video to upload


# Main function
if __name__ == "__main__":
    while True:
        # Set up browser and login
        browser, page = setup_browser()
        driver = webdriver.Chrome()
        login(driver)

        # Download video and save as final.mp4
        video_title = download_video(page)
        page.close()
        browser.close()
        os.rename(os.path.expanduser("~/Downloads/{}.mp4".format(video_title)), "final.mp4")

        # Upload video to YouTube
        driver = webdriver.Chrome()
        upload_video(driver, video_title)
        driver.quit()

        # Wait for an hour before repeating the process
        time.sleep(60*60)
