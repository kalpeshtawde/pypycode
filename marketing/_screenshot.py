import sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/facebook_feed_ad_pricing.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 1400}, device_scale_factor=2)
    page.goto(URL)
    page.wait_for_timeout(1200)  # let fonts load
    el = page.query_selector(".ad-square")
    box = el.bounding_box()
    computed = page.evaluate(
        "() => { const e = document.querySelector('.ad-square'); const r = getComputedStyle(e); return {height: r.height, width: r.width}; }"
    )
    print(f"bounding_box: width={box['width']} height={box['height']}")
    print(f"computed: width={computed['width']} height={computed['height']}")
    el.screenshot(path="ad_preview.png")
    print("screenshot saved: ad_preview.png")
    browser.close()
