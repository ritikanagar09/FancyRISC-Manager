import sys

from errors import Logger, check_cat, check_variant
from reader import find_cat, find_variant, encode
from memory import Memory

err = Logger()

commands = []
mem0 = len([x for x in sys.stdin if x.strip() != ''])

mem = Memory(mem0)
PC = 0
for line_num, line in enumerate(sys.stdin):
	line = line.strip()

	variant = find_variant(line)
	error = check_variant(variant, line)

	if variant == 'blank':
		continue

	PC += 1  # doesn't include blank lines

	if variant == 'label':  # will always be followed by instruction
		mem.store_label(line.split(':')[0], PC)

	if variant in ('label','instruction'):  # common handler for instructions with and without label
		# category identification
		cat = find_cat(line)  
		error = check_cat(cat, line, mem) 
	
		# error handling
		if (error[0] == True):
			err.log(line_num, error)
			continue

		# encoding 
		buffer = encode(cat, line, mem)

		commands.append(buffer)

	elif variant == 'variable':
		mem.store_var(line[4:]) # excluding 'var '

