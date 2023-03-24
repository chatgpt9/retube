import os
from playwright.sync_api import Playwright, sync_playwright
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VIDEO_INDEX_URL = "https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ/videos"
VIDEO_SELECTOR = "#video-title"
VIDEO_DOWNLOAD_URL = "https://www.onlinevideoconverter.com/youtube-converter"
VIDEO_DOWNLOAD_SELECTOR = "#texturl"
VIDEO_DOWNLOAD_BUTTON = "//button[contains(@class, 'btn-primary')]"
FINAL_VIDEO_PATH = "/path/to/final.mp4"
GMAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def download_video():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(VIDEO_INDEX_URL)
        video_title = page.query_selector(VIDEO_SELECTOR).text_content()
        page.click(VIDEO_SELECTOR)
        page.wait_for_selector(VIDEO_DOWNLOAD_SELECTOR)
        page.fill(VIDEO_DOWNLOAD_SELECTOR, page.url)
        page.click(VIDEO_DOWNLOAD_BUTTON)
        page.wait_for_navigation()
        page.click("[name='submit']")
        page.wait_for_selector("[aria-describedby='download-result']")
        download_url = page.query_selector("[aria-describedby='download-result'] a").get_attribute("href")
        page.close()
        browser.close()
    os.system(f"wget -O {FINAL_VIDEO_PATH} {download_url}")
    print(f"Downloaded {video_title} as final.mp4")

def upload_video():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/upload")
    driver.find_element(By.ID, "identifierId").send_keys(GMAIL_USERNAME + Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    driver.find_element(By.NAME, "password").send_keys(GMAIL_PASSWORD + Keys.ENTER)
    driver.find_element(By.NAME, "Filedata").send_keys(FINAL_VIDEO_PATH)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "privacy-public")))
    driver.find_element(By.ID, "privacy-public").click()
    driver.find_element(By.ID, "next-button").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "done-button")))
    driver.find_element(By.ID, "done-button").click()
    driver.quit()
    print(f"Uploaded {FINAL_VIDEO_PATH} to YouTube")

if __name__ == "__main__":
    download_video()
    upload_video()
