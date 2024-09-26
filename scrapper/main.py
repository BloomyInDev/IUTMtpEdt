from time import sleep
from tsv_parser import ParseTSV

from playwright.sync_api import Browser, Page
from playwright.sync_api import sync_playwright

TSV_NAME: str = "liens_edt.tsv"

URLS: dict[int, str] = ParseTSV(TSV_NAME, True)

with sync_playwright() as p:
	browser: Browser = p.webkit.launch()
	page: Page = browser.new_page()
	page.goto(URLS[1])
	print("goto")
	sleep(15)
	page.screenshot(path="example.png")
	browser.close()

