from time import sleep
from typing import Any
from tsv_parser import ParseTSV
from json import dump

from playwright.sync_api import Browser, Page
from playwright.sync_api import sync_playwright

from bs4 import ResultSet, Tag
from bs4 import BeautifulSoup


TSV_NAME: str = "liens_edt.tsv"

URLS: dict[int, str] = ParseTSV(TSV_NAME, True)


def find_divs(css_class: str | None):
    return css_class is not None and css_class.startswith("div")

def remove_spaces_in_list(list:list[str]):
    cl = list.copy()
    i = 0
    while i < len(cl):
        if (cl[i] == ""):
            cl.pop(i)
        else:
            i+=1
    return cl

with sync_playwright() as p:
    print("Starting Browser (WebKit)")
    browser: Browser = p.webkit.launch()
    page: Page = browser.new_page()
    page.goto(URLS[1])
    print("Page loading")
    sleep(15)
    page.screenshot(path="example.png")
    print("Dumping page")
    pageDump: str = page.content()
    with open("page.html", "w") as f:
        f.write(pageDump)
    browser.close()

    soup = BeautifulSoup(pageDump, "lxml")

    events: ResultSet[Tag] = soup.find_all("div", id=find_divs)

    parsedEvents: list[Any] = []
    for event in events:
        content = event.contents[0]
        raw_data: list[str] = content["aria-label"].split("null")
        parsedEvents.append(
            raw_data
        )
    with open("result.json") as f:
        dump(parsedEvents,f)
