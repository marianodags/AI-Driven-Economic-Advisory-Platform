import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        await page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        await asyncio.sleep(1)

        # Click "AI Insights & Simulator" tab
        await page.click("button:has-text('AI Insights & Simulator')")
        await asyncio.sleep(1)

        # Click "Re-Run Policy Simulation" button
        await page.click("button:has-text('Re-Run Policy Simulation')")
        await asyncio.sleep(1.5)

        await page.screenshot(path="verified_policy_simulator.png")
        print("Screenshot saved to verified_policy_simulator.png")

        await browser.close()

asyncio.run(run())
