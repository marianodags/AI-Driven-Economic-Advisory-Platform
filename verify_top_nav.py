import time, os
from playwright.sync_api import sync_playwright

def verify():
    # Start flask server in background
    import subprocess
    server_process = subprocess.Popen(["python3", "main.py"])
    time.sleep(3)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:5000", wait_until="networkidle")

            # Capture screenshot of Executive Overview with top nav
            page.screenshot(path="verified_top_navbar.png")
            print("Captured verified_top_navbar.png screenshot successfully.")

            # Switch to 2026-2030 Forecasts tab
            page.click("button:has-text('2026–2030 Forecasts')")
            time.sleep(0.5)

            # Switch to Industry Sectors tab
            page.click("button:has-text('Industry Sectors & Analytics')")
            time.sleep(0.5)

            browser.close()
    finally:
        server_process.terminate()

if __name__ == "__main__":
    verify()
