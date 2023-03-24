import os
from playwright.sync_api import Playwright, sync_playwright

# Set environment variables for Gmail and Youtube credentials
gmail_username = os.getenv('GMAIL_USERNAME')
gmail_password = os.getenv('GMAIL_PASSWORD')
youtube_username = os.getenv('YOUTUBE_USERNAME')
youtube_password = os.getenv('YOUTUBE_PASSWORD')

# Define function to download video from Youtube index page
def download_video(page):
    # Navigate to Youtube index page
    page.goto('https://www.youtube.com')
    # Find the first video link and click on it
    video_link = page.locator('#thumbnail').first()
    video_link.click()
    # Wait for video to load and click on download button
    page.wait_for_selector('#buttons .ytp-download-button')
    download_button = page.locator('#buttons .ytp-download-button')
    download_button.click()
    # Wait for download to finish and return the downloaded file path
    page.wait_for_download()
    return page.context().downloads_folder().get_downloaded_file_path()

# Define function to upload video to Youtube
def upload_video(page, video_path):
    # Navigate to Youtube upload page
    page.goto('https://www.youtube.com/upload')
    # Fill in Youtube login credentials and submit
    page.fill('#identifierId', youtube_username)
    page.click('#identifierNext')
    page.fill('#password input', youtube_password)
    page.click('#passwordNext')
    # Wait for upload page to load and select file to upload
    page.wait_for_selector('#upload-prompt-box input[type="file"]')
    upload_input = page.locator('#upload-prompt-box input[type="file"]')
    upload_input.set_input_files(video_path)
    # Wait for video to upload and fill in title and description
    page.wait_for_selector('#textbox')
    page.fill('#textbox', 'My uploaded video')
    page.fill('#description', 'This is my first uploaded video')
    # Click on publish button
    page.click('#publish-button')

# Run the script
with sync_playwright() as playwright:
    # Set up browser and page context
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    # Log in to Gmail
    page.goto('https://www.gmail.com')
    page.fill('#identifierId', gmail_username)
    page.click('#identifierNext')
    page.fill('#password input', gmail_password)
    page.click('#passwordNext')
    # Download video and upload it to Youtube
    video_path = download_video(page)
    upload_video(page, video_path)
    # Clean up resources
    context.close()
    browser.close()
