import sys

from errors import Logger, check_cat, check_variant
from reader import find_cat, find_variant, encode
from memory import Memory

err = Logger()

commands = []
fl = []
for line in sys.stdin:
	fl.append(line)

#fl = sys.stdin
#fl = "var X\nadd r1 r2 r3 r4\nvar y\n hlt now\n hello: add r1 r2 r3".split('\n')
#with open('testing.txt') as txt:
#	fl = txt.read().split('\n')

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
		continue 

	if variant == 'blank':
		continue

	if variant == 'variable':
		mem.store_var(line[4:]) # excluding 'var '
		continue

	PC += 1  # doesn't include blank lines and variable definitions

PC = 0
# SECOND PASS
for line_num, line in enumerate(fl): 
	# am i not on the last line?
	lookahead = len([1 for x in fl[line_num:] if x.strip() != '']) > 1 # are there any non-blank lines ahead of this line
	line = line.strip() 

	if(not lookahead):
		if(not line.endswith('hlt')):
			err.log_error(line_num+1,['hlt not present at end of code'])

	variant = find_variant(line)
	error = check_variant(variant, line, PC)

	if variant == 'label':  # will always be followed by instruction
		# Turns label into instruction 'labelname: add R0 R1 R2' => 'add R0 R1 R2'
		line = line.split(':')[1].lstrip()  
		variant = find_variant(line)
		check_variant(variant, line, PC)
	
	if (error[0] == True):  # variant error handling
		err.log_error(line_num+1, error[1])
		continue # stop processing the line here, go to the next line

	if variant == 'blank' or variant == 'variable':
		continue

	PC += 1  # doesn't include blank lines and variable definitions

	if variant in ('label','instruction'):  # common handler for instructions with and without label
		# category identification
		opc, cat = find_cat(line)['opcode'], find_cat(line)['cat'] # 'add R0 R1 R2' => {'opcode':0,'cat':'A'}
		
		#print(f'{line_num}: {lookahead}')
		error = check_cat(opc, cat, line, mem, lookahead) 
	
		# handles instruction category-specific errors
		if (error[0] == True):
			err.log_error(line_num+1, error[1])
			continue

		# encoding 
		buffer = encode(opc, cat, line, mem)  # Input - 0, A, add R0 R1 R2, mem ; Out -> 010010101010101

		commands.append(buffer) # ['000100','0110101','011101','010011'] <- all will be 16 bits

if err.errors_present():
	print('\n'.join(err.get_errors()))
else:
	print('\n'.join(commands))