import sys

from errors import Logger, check_cat, check_variant
from reader import find_cat, find_variant, encode

err = Logger()
commands = []

for line_num, line in enumerate(sys.stdin):
	variant = find_variant(line)  
	error = check_variant(variant, line)  

	if variant == 'label':  # will always be followed by instruction
		pass

	if variant in ('label','instruction'):  # common handler for instructions with and without label
		# category identification
		cat = find_cat(line)  
		error = check_cat(cat, line) 
	
		# error handling
		if (error[0] == True):
			err.log(line_num, error)
			continue

		# encoding 
		buffer = encode(cat, line)

		commands.append(buffer)

	elif variant == 'variable':
		pass

