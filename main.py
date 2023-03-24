import os
from playwright.sync_api import Playwright, sync_playwright

async def download_and_upload_video(page, video_index):
    # Navigate to the YouTube homepage
    await page.goto('https://www.youtube.com')

    # Click on the video at the specified index
    video_links = await page.query_selector_all('a#video-title')
    await video_links[video_index].click()

    # Wait for the video player to load and then click on the download button
    await page.wait_for_selector('button.ytp-download-button')
    await page.click('button.ytp-download-button')

    # Wait for the download to finish and then get the file path
    download_path = await page.wait_for_download()

    # Rename the downloaded file to final.mp4
    os.rename(download_path, 'final.mp4')

    # Navigate to the YouTube upload page
    await page.goto('https://www.youtube.com/upload')

    # Upload the video file
    await page.set_input_files('input[type="file"]', 'final.mp4')
    await page.wait_for_selector('button#upload-prompt-box-upload-button')
    await page.click('button#upload-prompt-box-upload-button')

    # Fill in the video title and description
    await page.fill('input#textbox', 'My Video Title')
    await page.fill('textarea#textarea', 'My Video Description')

    # Sign in to your Google account
    await page.fill('input#identifierId', os.environ['GMAIL_USERNAME'])
    await page.click('button#identifierNext')
    await page.fill('input[name="password"]', os.environ['GMAIL_PASSWORD'])
    await page.click('button#passwordNext')

    # Wait for the video to finish uploading and then close the browser
    await page.wait_for_selector('ytcp-video-upload-progress')
    await browser.close()

# Main function
async def main():
    # Set up Playwright
    async with sync_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        # Download and upload the video every hour
        while True:
            await download_and_upload_video(page, 0)
            await page.wait_for_timeout(3600000) # Wait for 1 hour before repeating

if __name__ == '__main__':
    asyncio.run(main())
