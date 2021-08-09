import sys

from errors import Logger, check_cat, check_variant
from reader import find_cat, find_variant, encode
from memory import Memory

err = Logger()

commands = []
#fl = sys.stdin
fl = "var x\nadd $1 $2".split('\n')

# only include instructions in memory count
mem0 = len([x for x in fl if x.strip() != '' and not x.strip().startswith('var')])

mem = Memory(mem0)
PC = 0
for line_num, line in enumerate(fl):
	line = line.strip()

	variant = find_variant(line)
	error = check_variant(variant, line, PC)

	if (error[0] == True):  # variant error handling
		err.log_error(line_num, error[1])
		continue 

	if variant == 'blank':
		continue

	if variant == 'variable':
		mem.store_var(line[4:]) # excluding 'var '

	PC += 1  # doesn't include blank lines and variable definitions

	if variant == 'label':  # will always be followed by instruction
		mem.store_label(line.split(':')[0], PC)

	if variant in ('label','instruction'):  # common handler for instructions with and without label
		# category identification
		cat = find_cat(line)  
		error = check_cat(cat, line, mem) 
	
		# category error handling
		if (error[0] == True):
			err.log_error(line_num, error[1])
			continue

		# encoding 
		buffer = encode(cat, line, mem)

		commands.append(buffer)

print('\n'.join(err.get_errors()))

