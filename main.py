import os
import time
from playwright.sync_api import Playwright, sync_playwright

async def main(playwright: Playwright):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    # Navigate to YouTube
    await page.goto('https://www.youtube.com')

    # Wait for the latest video to load
    await page.wait_for_selector('#thumbnail')

    # Get the URL of the latest video
    video_url = await page.get_attribute('a#thumbnail', 'href')

    # Download the video
    await page.goto(video_url)
    await page.wait_for_selector('.ytp-large-play-button')
    await page.click('.ytp-large-play-button')
    time.sleep(10)  # Wait for the video to start playing
    await page.keyboard.press('f')  # Switch to fullscreen
    time.sleep(10)  # Wait for the video to play in fullscreen
    await page.keyboard.press('d')  # Download the video
    time.sleep(10)  # Wait for the download to finish

    # Rename the downloaded video to 'final.mp4'
    os.rename('video.mp4', 'final.mp4')

    # Upload the video to YouTube
    await page.goto('https://studio.youtube.com')
    await page.wait_for_selector('#upload-button')
    await page.click('#upload-button')
    await page.wait_for_selector('input[type=file]')
    await page.set_input_files('input[type=file]', 'final.mp4')
    await page.wait_for_selector('#next-button')
    await page.click('#next-button')
    await page.wait_for_selector('#title')
    await page.fill('#title', 'My video title')
    await page.wait_for_selector('#next-button')
    await page.click('#next-button')
    await page.wait_for_selector('#done-button')
    await page.click('#done-button')

    # Close the browser
    await browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        playwright.run(main)
