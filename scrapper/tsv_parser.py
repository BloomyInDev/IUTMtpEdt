def OpenRawTSV(tsv_name: str) -> str:
	file = open(tsv_name, "r", encoding="utf8")
	raw_text = file.read()
	file.close()

	del file

def ParseRawText(raw_text: str, header_line: bool=True) -> dict[int: str]:
	lines: list[str] = raw_text.split("\n")

	output: dict[int: str] = {}

	if (header_line):
		lines.remove(lines[0])

	while ("" in lines):
		lines.remove("")

	for l in lines:
		l: list[str] = l.split("\t")

		year_id: int = int(l[0])
		url: str = l[1]

		output[year_id] = url

	return output

def ParseTSV(tsv_filename: str, header_line: bool=True) -> dict[int: str]:
	"""
		Input	: tsv_filename	(str, self explanatory)
				: header_line		(bool, is there a line with columns' name)

		Output	: dict[int: str], The int is the year, the str is the planning's url
	"""

	raw_text: str = OpenRawTSV(tsv_filename)
	output: dict[int: str] = dict(ParseRawText(raw_text, header_line))

	return output
