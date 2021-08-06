import json

def find_variant(line):
	return "instruction"


insts = json.load(open('instructions.json'))
def find_cat(cmd):
	"finds what category a specific command belongs to, and its opcode"

	params = cmd.split()

	if len(params) == 0 or params[0] not in insts:
		return {'opcode':0b11111, 'cat':'unidentified'}
	if params[0] not in insts:  # invalid instruction type
		return {'opcode':0b11111, 'cat':'unidentified'}

	opcode = int(insts[params[0]]['opcode'],base = 2)
	cat = 'A'
	return {'opcode':opcode, 'cat':cat}


cats = json.load(open('categories.json'))
def encode(ctg,cmd):
	"encodes command according to its category"

	return 0b01000111101110
