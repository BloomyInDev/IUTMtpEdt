def openRawTSV(tsv_name: str) -> str:
	file = open(tsv_name, "r", encoding="utf8")
	raw_text = file.read()
	file.close()

	del file

	return raw_text

def parseRawText(raw_text: str, header_line: bool=True) -> dict[str: str]:
	lines: list[str] = raw_text.split("\n")

	output: dict[str: str] = {}

	if (header_line):
		lines.remove(lines[0])

	while ("" in lines):
		lines.remove("")

	for l in lines:
		l: list[str] = l.split("\t")

		classe: str = l[0]
		url: str = l[1]

		output[classe] = url

	return output

def parseTSV(tsv_filename: str, header_line: bool=True) -> dict[str: str]:
	"""
		Input	: tsv_filename	(str, self explanatory)
				: header_line		(bool, is there a line with columns' name)

		Output	: dict[int: str], The int is the year, the str is the planning's url
	"""

	raw_text: str = openRawTSV(tsv_filename)
	output: dict[str: str] = dict(parseRawText(raw_text, header_line))

	return output
