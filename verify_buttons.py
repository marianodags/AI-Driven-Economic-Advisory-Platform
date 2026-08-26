import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        await page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        await asyncio.sleep(1)

        # Click "Run ML Forecaster" button in header
        await page.click("button:has-text('Run ML Forecaster')")
        await asyncio.sleep(1.5)

        # Click "Generate AI Insights" button in header
        await page.click("button:has-text('Generate AI Insights')")
        await asyncio.sleep(1.5)

        await page.screenshot(path="verified_ml_buttons.png")
        print("Screenshot saved to verified_ml_buttons.png")

        await browser.close()

asyncio.run(run())
