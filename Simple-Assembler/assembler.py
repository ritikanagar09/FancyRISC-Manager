from errors import Logger, check
from reader import identify, parse
import sys

err = Logger()
commands = []

for line_num, line in enumerate(sys.stdin):
	category = identify(line)
	error = check(category, line)
	
	if (error[0] == True):  # Error is found
		err.log(line_num, error)
		continue

	buffer = parse(category, line)

	commands.append(buffer)
