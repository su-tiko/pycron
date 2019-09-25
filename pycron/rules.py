import os
import collections

EXPRESSIONS = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *"
}


class ParseException(Exception):
    pass


CronRule = collections.namedtuple('CronRule', 'schedule command')


class RuleParser:
    def __init__(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = ".crontab"

    def parse(self):
        if not os.path.isfile(self.filename):
            raise ParseException("File does not exist")

        with open(self.filename, "r") as f:
            rules = filter(lambda l: l is not None, map(self.__parse_line, f.readlines()))

        return rules

    def __parse_line(self, line):
        line = line.strip()

        if line.startswith("@"):
            line = self.__parse_expr(line)

        line = line.split()

        if len(line) < 6:
            return None

        schedule = " ".join(line[0:5])
        command = " ".join(line[5:])

        return CronRule(schedule, command)

    def __parse_expr(self, line):
        line_data = line.split()
        line_expr = line_data[0]

        if len(line_data) < 2:
            raise ParseException("Invalid format")  # TODO: Add line number info

        if line_expr not in EXPRESSIONS:
            raise ParseException("Invalid expression")  # TODO: Add line number info

        return EXPRESSIONS[line_expr] + " " + " ".join(line_data[1:])
