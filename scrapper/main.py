from typing import Any
from edt import scrape_edt
import db


def get_profs(data: list[dict[str, Any]])->list[dict[str,str]]:
	profs = []
	for event in data:
		for prof in event["profs"]:
			prof:str = prof
			if not (prof in profs):
				profs.append(
					{
						"raw": prof,
						"firstname": prof.split(" ")[1],
						"lastname": prof.split(" ")[0],
					}
				)
	return profs


if __name__ == "__main__":
	edt = scrape_edt()

	prof_db = db.Professor()
	profs = get_profs(edt)
	for prof in profs:
		prof_db.add(prof["firstname"],prof["lastname"])
	print("Done adding profs !")

	event_db = db.Event()
	for event in edt:
		prepared_profs = []
		for prof in event["profs"]:
			prof = {
				"raw": prof,
				"firstname": prof.split(" ")[1],
				"lastname": prof.split(" ")[0],
			}
			prepared_profs.append((prof["lastname"],prof["firstname"]))
		event_db.add(event["name"], event["startTime"], event["endTime"], prepared_profs, event["students"], event["place"], event["color"])
	print("Done adding events !")
	#print(prof_db.get_all_names())

