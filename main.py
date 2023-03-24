import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import Playwright, sync_playwright

# Set up environment variables
email = os.environ.get('GMAIL_EMAIL')
password = os.environ.get('GMAIL_PASSWORD')

# Initialize Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Navigate to YouTube index page
    page.goto('https://www.youtube.com')

    # Wait for page to load
    page.wait_for_selector('#search')

    # Get the first video from the index page
    video = page.query_selector('#contents ytd-rich-item-renderer')

    # Get the video link and title
    video_link = video.query_selector('#thumbnail').get_attribute('href')
    video_title = video.query_selector('#title').text_content()

    # Download the video
    with open('final.mp4', 'wb') as f:
        f.write(page.goto(video_link).body())

    # Quit Playwright
    browser.close()

# Initialize Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Log in to YouTube
driver.get('https://accounts.google.com/signin')
driver.find_element_by_id('identifierId').send_keys(email)
driver.find_element_by_id('identifierNext').click()
time.sleep(1)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_id('passwordNext').click()
time.sleep(1)

# Upload the video to YouTube
driver.get('https://www.youtube.com/upload')
driver.find_element_by_id('file-picker').send_keys(os.path.abspath('final.mp4'))
driver.find_element_by_id('textbox').send_keys(video_title)
driver.find_element_by_id('next-button').click()
time.sleep(1)
driver.find_element_by_id('next-button').click()
time.sleep(1)
driver.find_element_by_id('done-button').click()

# Quit Selenium
driver.quit()
