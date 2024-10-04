from time import sleep
from tsv_parser import parseTSV
from json import dump
from datetime import datetime

from playwright.sync_api import Browser, Page
from playwright.sync_api import sync_playwright

from bs4 import ResultSet, Tag
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------

TSV_NAME: str = "liens_edt.tsv"

URLS: dict[str, str] = parseTSV(TSV_NAME, True)

DAYS = [
	"#x-auto-14 > tbody .x-btn-mc > em > button",
	"#x-auto-15 > tbody .x-btn-mc > em > button",
	"#x-auto-16 > tbody .x-btn-mc > em > button",
	"#x-auto-17 > tbody .x-btn-mc > em > button",
	"#x-auto-18 > tbody .x-btn-mc > em > button",
]

# ---------------------------------------------------------------------


def find_divs(css_class: str | None):
	return (css_class != None) and (css_class.startswith("div"))


def click_btn(page: Page, selector: str):
	return page.evaluate(
		f"""
	async () => {{
		const btn = document.querySelector("{selector}");
		btn.click();
		await new Promise(r => setTimeout(r, 5000));
	}}
	"""
	)


def parse_edt(page: Page, url: str):
	page.goto(url)
	print("Page loading")
	page.wait_for_selector("div#Planning", timeout=60000)
	sleep(2)

	data: dict[str : dict[str : str | list[str]]] = {}

	for i in range(len(DAYS)):
		click_btn(page, DAYS[i])
		pageDump: str = page.content()
		d = parse_page(pageDump)
		print(f"Day {d['day']} parsed successfully !")
		data[d["day"]] = d

	return data


def parse_page(pageContent: str):
	soup = BeautifulSoup(pageContent, "lxml")
	day = soup.find("div", id="4", class_="labelLegend")
	events: ResultSet[Tag] = soup.find_all("div", id=find_divs)

	rawEvents: list[list[dict[str,list[str],str]]] = []

	for event in events:
		content = event.contents[0]
		raw_data: list[str] = content["aria-label"].split(" null ")

		bgcolor = "#ffffff"
		styles = event.parent.parent.select_one("table").attrs["style"].split(";")
		for style in styles:
			if (style.startswith("background-color")):
				bgcolor = style.split(":")[-1]

		
		rawEvents.append({"raw":raw_data,"col":bgcolor})

	parsedEvents: list[dict[str, str | int]] = []
	newRawEvents = rawEvents.copy()
	
	for e in newRawEvents:
		event = e["raw"]
		dataDict = {}
		tempForName = event.pop(0)

		if tempForName.startswith(" "):
			tempForName = tempForName.split(" ", 1)[1]
		
		dataDict["name"] = tempForName
		tempTimeStart, tempEndTime = event.pop(-1).split(" - ")
		tempDate = day.text.split(" ")[1]
		
		dataDict["startTime"] = int(datetime(
			int(tempDate.split("/")[2]),
			int(tempDate.split("/")[1]),
			int(tempDate.split("/")[0]),
			int(tempTimeStart.split("h")[0]),
			int(tempTimeStart.split("h")[1]),
		).timestamp())
		dataDict["endTime"] = int(datetime(
			int(tempDate.split("/")[2]),
			int(tempDate.split("/")[1]),
			int(tempDate.split("/")[0]),
			int(tempEndTime.split("h")[0]),
			int(tempEndTime.split("h")[1]),
		).timestamp())
		
		dataDict["profs"] = []
		tempForPlace = []
		
		if len(event) > 2:
			tempForPlace.append(event.pop(0))
			tempForPlace.append(event.pop(0))
			tempPlace = ""

			if tempForPlace[1] == "":
				pass

			elif "/" in tempForPlace[1]:
				tempPlace = f'Campus {tempForPlace[1].split("/")[0]}- Batiment {tempForPlace[1].split(" / ")[-2]} - '

			else:
				tempPlace = f"Campus {tempForPlace} - "
			
			tempPlace += tempForPlace[0]
			dataDict["place"] = tempPlace
		
		else:
			dataDict["place"] = "Pas de salle"
		
		while any("   " in d for d in event):
			i = 0
			while i < len(event):
				if "   " in event[i]:
					dataDict["profs"].append(
						event.pop(i)
						.replace("   ", "&")
						.replace(" ", "-")
						.replace("&", " ")
					)

				else:
					i += 1
		dataDict["students"] = event.copy()
		dataDict["color"]=e["col"]

		parsedEvents.append(dataDict)

	return {"day": day.text.split(" ")[1], "event": parsedEvents}


with sync_playwright() as p:
	print("Starting Browser (WebKit)")
	browser: Browser = p.webkit.launch(headless=False)
	page: Page = browser.new_page()

	data: dict[str, dict[str : dict[str : str | list[str]]]] = {}

	#for key in URLS.keys():
	for key in ["S4"]:
		data[key] = parse_edt(page, URLS[key])
	browser.close()

	with open("result.json", "w") as f:
		dump(data, f, indent=4)
