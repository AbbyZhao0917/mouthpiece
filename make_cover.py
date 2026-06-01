from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath("cover.html")
out_path = os.path.expanduser("~/Downloads/嘴替封面.png")

with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page(viewport={"width": 750, "height": 1000})
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(1500)   # 等字体和渐变加载
    page.screenshot(path=out_path, full_page=False)
    browser.close()

print(f"✅ 已保存到：{out_path}")
