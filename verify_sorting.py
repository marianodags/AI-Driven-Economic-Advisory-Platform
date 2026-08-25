import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        await page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        await asyncio.sleep(1)

        # Click Industry Sectors & Analytics
        await page.click("button:has-text('Industry Sectors & Analytics')")
        await asyncio.sleep(1)

        # Select Growth Rate (All Industries)
        await page.click("button:has-text('2. Growth Rate (All Industries)')")
        await asyncio.sleep(1)

        # Click "Top Growth Rate" sorting button
        await page.click("#btnSortGrowth")
        await asyncio.sleep(1)

        await page.screenshot(path="verified_sort_growth.png")
        print("Screenshot saved to verified_sort_growth.png")

        await browser.close()

asyncio.run(run())
