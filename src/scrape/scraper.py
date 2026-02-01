# scraper.py
import asyncio
from playwright.async_api import async_playwright


async def scrape(url: str) -> str:
    async with async_playwright() as p:
        # launch Chromium in headless mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        # extract page content (you can use CSS selectors, XPath, etc.)
        content = await page.inner_text("body")
        await browser.close()
        return content

if __name__ == "__main__":
    url = "https://example.com"
    html = asyncio.run(scrape(url))
    print(html[:500])          # print first 500 characters
