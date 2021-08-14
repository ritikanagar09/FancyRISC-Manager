import sys

from errors import Logger, check_cat, check_variant
from reader import find_cat, find_variant, encode
from memory import Memory

err = Logger()

commands = []
#fl = sys.stdin
#fl = "var X\nadd r1 r2 r3 r4\nvar y\n hlt now\n hello: add r1 r2 r3".split('\n')
with open('testing.txt') as txt:
	fl = txt.read().split('\n')

# only include instructions in memory count
mem0 = len([x for x in fl if x.strip() != '' and not x.strip().startswith('var')])

mem = Memory(mem0)
PC = 0

# FIRST PASS
for line_num, line in enumerate(fl):  
	line = line.strip() 

	variant = find_variant(line)
	error = check_variant(variant, line, PC)

	if variant == 'label':  # will always be followed by instruction
		mem.store_label(line.split(':')[0], PC)
	
	if (error[0] == True):  # variant error handling
		err.log_error(line_num+1, error[1])
		continue 

	if variant == 'blank':
		continue

	if variant == 'variable':
		mem.store_var(line[4:]) # excluding 'var '
		continue

	PC += 1  # doesn't include blank lines and variable definitions

PC = 0
# SECOND PASS
for line_num, line in enumerate(fl):  # SECOND PASS
	line = line.strip() 

	variant = find_variant(line)
	error = check_variant(variant, line, PC)

	if variant == 'label':  # will always be followed by instruction
		# Turns label into instruction
		line = line.split(':')[1].lstrip()  
		variant = find_variant(line)
		check_variant(variant, line, PC)
	
	if (error[0] == True):  # variant error handling
		err.log_error(line_num+1, error[1])
		continue 

	if variant == 'blank' or variant == 'variable':
		continue

	PC += 1  # doesn't include blank lines and variable definitions

	if variant in ('label','instruction'):  # common handler for instructions with and without label
		# category identification
		opc, cat = find_cat(line)['opcode'], find_cat(line)['cat']
		lookahead = len([1 for x in fl[line_num:] if x.strip() != '']) > 1
		error = check_cat(cat, line, mem, lookahead) 
	
		# handles instruction category-specific errors
		if (error[0] == True):
			err.log_error(line_num+1, error[1])
			continue

		# encoding 
		buffer = encode(opc, cat, line, mem)

		commands.append(buffer)

if err.errors_present():
	print('\n'.join(err.get_errors()))
else:
	print('\n'.join(commands))

