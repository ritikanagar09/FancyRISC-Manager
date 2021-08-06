import sys

from errors import Logger, check_category, check_variant
from reader import identify_category, identify_variant, parse

err = Logger()
commands = []

for line_num, line in enumerate(sys.stdin):
	variant = identify_variant(line)  # Identifies the variant of command
	error = check_variant(variant, line)  # Checks for broad syntax errors

	if variant == 'label':  # Will always be followed by instruction
		pass

	if variant in ('label','instruction'):  # Common handler for instructions with and without label
		category = identify_category(line)  # Identifies type of instruction
		error = check_category(category, line)  # Checks if instruction fits the type
	
		if (error[0] == True):  # Error is found
			err.log(line_num, error)
			continue

		buffer = parse(category, line)

		commands.append(buffer)

	elif variant == 'variable':
		pass

	elif variant == 'label':
		pass
