from typing import Any
from edt import scrape_edt
from db import Professor as ProfessorInDb


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
	prof_db = ProfessorInDb()
	profs = get_profs(edt)
	for prof in profs:
		prof_db.add(prof["firstname"],prof["lastname"])
	print("Done adding profs !")
	print(prof_db.get_all_names())
