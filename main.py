import os
from playwright.sync_api import Playwright, sync_playwright

async def download_video():
    async with sync_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.youtube.com/")
        await page.click("#search")
        await page.type("#search", "daily one video")
        await page.press("#search", "Enter")
        await page.click("#contents #thumbnail")
        await page.click("#meta-contents #subscribe-button")
        await page.click("#meta-contents #menu-container #top-level-buttons #button")
        await page.click("#items #items #label")
        await page.click("#items #items #button")
        await page.wait_for_selector("#dialog #confirm-button")
        await page.click("#dialog #confirm-button")
        await page.wait_for_selector("#progress #progress-text")

        # Rename downloaded file as final.mp4
        downloaded_file = os.path.expanduser("~/Downloads/video.mp4")
        final_file = os.path.expanduser("~/Downloads/final.mp4")
        os.rename(downloaded_file, final_file)

    await upload_video(final_file)

async def upload_video(final_file):
    async with sync_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.youtube.com/upload")
        await page.wait_for_selector("#start-upload #file-upload-button")
        file_input = await page.query_selector("#start-upload #file-upload-button")
        await file_input.set_input_files(final_file)
        await page.wait_for_selector("#start-upload #next-button")
        await page.click("#start-upload #next-button")
        await page.wait_for_selector("#video-properties #title")
        await page.fill("#video-properties #title", "Daily video upload")
        await page.click("#video-properties #privacy-button")
        await page.click("#video-properties #privacy-menu .ytp-menuitem:nth-child(1)")
        await page.wait_for_selector("#video-properties #publish-button")
        await page.click("#video-properties #publish-button")
        await page.wait_for_selector("#upload-progress #text")
        print("Video uploaded successfully.")

if __name__ == "__main__":
    # Set environment variables for Gmail and password
    os.environ["GMAIL_USERNAME"] = "chatgpt8k@gmail.com"
    os.environ["GMAIL_PASSWORD"] = "tJ19dQzWWH4THIWb"

    # Call the function to download and upload video
    download_video()
