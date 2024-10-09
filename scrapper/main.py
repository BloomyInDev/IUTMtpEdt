from time import sleep, perf_counter
from tsv_parser import parseTSV
from json import dump
from datetime import datetime

from pprint import pprint

from playwright.sync_api import Browser, Page
from playwright.sync_api import sync_playwright

from bs4 import ResultSet, Tag
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------

TSV_NAME: str = "liens_edt.tsv"

URLS: dict[str, str] = parseTSV(TSV_NAME, True)

# ---------------------------------------------------------------------


def find_divs(css_class: str | None):
	return (css_class != None) and (css_class.startswith("div"))


def click_btn(page: Page, selector: str):
	return page.evaluate(
		f"""
	async () => {{
		const btn = document.querySelector("{selector}");
		btn.click();
		await new Promise((resolve,reject)=>{{
		const a = setInterval(
			()=>{{
				if (document.querySelector("img.gwt-Image")==null) {{
					resolve()
					clearInterval(a)
				}}
			}},100)
		}})
	}}
	"""
	)


def click_next_week(page: Page):
	return page.evaluate(
		f"""
	async () => {{
		const btn = document.querySelector("#x-auto-{int(page.query_selector_all(".x-btn-pressed")[-1].get_attribute("id").split("-")[-1])+1} > tbody .x-btn-mc > em > button");
		btn.click();
		await new Promise((resolve,reject)=>{{
		const a = setInterval(
			()=>{{
				if (document.querySelector("img.gwt-Image")==null) {{
					resolve()
					clearInterval(a)
				}}
			}},100)
		}})
	}}
	"""
	)


def parse_edt(page: Page, url: str):
	print("\x1b[0KPage loading",end="\r")
	page.goto(url)
	print("\x1b[0KPage loaded",end="\r")
	page.wait_for_selector("div#Planning", timeout=60000)
	sleep(0.5)
	data = []

	# Loop to make
	loopsToMake = 2
	for i in range(loopsToMake):
		print(f"\x1b[0KParsing week {i+1}",end="\r")
		pageDump: str = page.content()
		data.extend(parse_page(pageDump))
		if i + 1 != loopsToMake:
			click_next_week(page)

	return data


def parse_page(pageContent: str):
	soup = BeautifulSoup(pageContent, "lxml")

	rawDays: list[Tag] = soup.find_all("div", class_="labelLegend")
	days = list(map(lambda x: x.contents[-1].split(" ")[-1], rawDays))[1:7]

	events: ResultSet[Tag] = soup.find_all("div", id=find_divs)
	rawEvents = []

	for event in events:
		rawData: list[str] = event.contents[0]["aria-label"].split(" null ").copy()

		# Search for "left" style
		styles = event.parent.get_attribute_list("style")[0]
		pos = -1
		for style in styles.replace(" ", "").split(";"):
			if style.startswith("left"):
				pos = int(style.split(":")[-1].strip("px"))//202
		if pos == -1:
			# If it wasn't found, the layout changed so its needs
			raise Exception("Pos should be modified here")
		
		result: dict[str, str | int] = {}

		result["name"] = rawData.pop(0).strip()

		tempTimeStart, tempEndTime = rawData.pop(-1).split(" - ")
		result["startTime"]=int(get_date(days[pos],tempTimeStart).timestamp())
		result["endTime"]=int(get_date(days[pos],tempEndTime).timestamp())

		result["profs"] = []
		tempForPlace = []

		if len(rawData) > 2:
			tempForPlace.append(rawData.pop(0))
			tempForPlace.append(rawData.pop(0))
			tempPlace = ""

			if tempForPlace[1] == "":
				pass

			elif "/" in tempForPlace[1]:
				tempPlace = f'Campus {tempForPlace[1].split("/")[0]}- Batiment {tempForPlace[1].split(" / ")[-2]} - '

			else:
				tempPlace = f"Campus {tempForPlace} - "

			tempPlace += tempForPlace[0]
			result["place"] = tempPlace
		else:
			result["place"] = "Pas de salle"
		
		while any("   " in d for d in rawData):
			i = 0
			while i < len(rawData):
				if "  " in rawData[i]:
					result["profs"].append(
						rawData.pop(i)
						.replace("   ", "&")
						.replace(" ", "-")
						.replace("&", " ")
					)

				else:
					i += 1

		result["students"] = rawData.copy()
		result["color"] = get_background_color(event)

		rawEvents.append(result)

	return rawEvents


def get_background_color(element: Tag):
	bgcolor = "#ffffff"
	styles = element.parent.parent.select_one("table").attrs["style"].split(";")
	for style in styles:
		if style.startswith("background-color"):
			bgcolor: str = style.split(":")[-1]
	return bgcolor


def get_date(date: str, time: str) -> datetime:
	return datetime(
		int(date.split("/")[2]),
		int(date.split("/")[1]),
		int(date.split("/")[0]),
		int(time.split("h")[0]),
		int(time.split("h")[1]),
	)


with sync_playwright() as p:
	print("Starting scrapper")
	print("\x1b[0KStarting Browser (Chromium)",end="\r")
	start = perf_counter()
	browser: Browser = p.chromium.launch(headless=True)
	page: Page = browser.new_page()

	data = []

	for key in URLS.keys():
	# for key in ["S4"]:
		data.extend(parse_edt(page, URLS[key]))
	browser.close()

	end = perf_counter()
	print(f"Scrapping done in {end-start}s")
	# pprint(data)
	with open("result.json","w") as f:
		dump(data, f, indent=4)
