import json

def find_variant(line):
	"find what variant of command is present in this line, and returns it"

	if line == '':
		return 'blank'
	if ':' in line[1:]: # and line[line.index(':')-1] != ' ':  
		return 'label'
	if line.startswith('var'):
		return 'variable'
	return 'instruction'


insts = json.load(open('instructions.json'))
def find_cat(cmd):
	"finds what category a specific command belongs to, and its opcode"

	params = cmd.split()

	if len(params) == 0 or params[0] not in insts:  # if invalid instruction category
		return {'opcode':0b11111, 'cat':'unidentified'}

	opcode = int(insts[params[0]][0]['opcode'],base = 2)
	cat = insts[params[0]][0]['type']
	
	if len(insts[params[0]]) > 1:  # very sloppy hard coding for mov instruction
		if params[2][0] == '$':
			opcode = int(insts[params[0]][1]['opcode'],base = 2) 
			cat = insts[params[0]][1]['type']
	
	return {'opcode':opcode, 'cat':cat}


cats = json.load(open('categories.json'))
def encode(ctg,cmd,mem):
	"encodes command according to its category"

	return 0b01000111101110
