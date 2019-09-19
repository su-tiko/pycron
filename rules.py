class ParseException(Exception):
	pass


class RuleParser: 
	EXPRESSIONS = {
		"@yearly": "0 0 1 1 *",
		"@annually": "0 0 1 1 *",
		"@monthly": "0 0 1 * *",
		"@weekly": "0 0 * * 0",
		"@daily": "0 0 * * *",
		"@midnight": "0 0 * * *",
		"@hourly": "0 * * * *"
	}

	def __init__(self, filename=None):
		if filename:
			self.filename = filename
		else:
			# TODO: Fix path
			self.filename = ".crontab"


	def parse(self):
		rules = []

		with open(self.filename, "r") as f:
			rules = map(self.__parse_line, f.readlines())


	def __parse_line(self, line):
		# TODO: Replace tabs for spaces

		if line.startswith("@"):
			line = self.__parse_expr(line)
		
		

	def __parse_expr(self, line):
		line_data = line.split()
		line_expr = line_data[0]

		if len(line_data) < 2:
			raise ParseException("Invalid format") # TODO: Add line number info

		if line_expr not in EXPRESSIONS:
			raise ParseException("Invalid expression") # TODO: Add line number info

		return EXPRESSIONS[line_expr] + " ".join(line_data[1:])
