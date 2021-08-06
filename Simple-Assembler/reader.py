import json

def find_variant(line):
	return "instruction"


insts = json.load('instructions.json')
def find_cat(cmd):
	"finds what category a specific command belongs to, and its opcode"

	params = cmd.split()

	if params[0] not in insts:  # invalid instruction type
		return {'opcode':0b11111, 'cat':'unidentified'}

	opcode = int(insts[params[0]]['opcode'])
	cat = 'A'
	return {'opcode':opcode, 'cat':cat}


cats = json.loads('categories.json')
def encode(ctg,cmd):
	"encodes command according to its category"

	return 0b01000111101110
