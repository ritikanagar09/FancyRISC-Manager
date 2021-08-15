import json
import memory

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
		#return 'unidentified'

	opcode = int(insts[params[0]][0]['opcode'],base = 2)
	cat = insts[params[0]][0]['type']
	
	if len(insts[params[0]]) > 1:  # very sloppy hard coding for mov instruction
		if params[2][0] != '$':
			opcode = int(insts[params[0]][1]['opcode'],base = 2) 
			cat = insts[params[0]][1]['type']
	
	#return cat
	return {'opcode':opcode, 'cat':cat}


cats = json.load(open('categories.json'))
def encode(opc,ctg,cmd,mem: memory.Memory):
	"encodes command according to its category"

	params = cmd.split()
	toret = ""
	
	if ctg == 'A':
		toret += f'{opc:05b}'
		toret += f'{0:02b}'
		toret += f'{int(params[1][1]):03b}'
		toret += f'{int(params[2][1]):03b}'
		toret += f'{int(params[3][1]):03b}'
	
	elif ctg == 'B':
		toret += f'{opc:05b}'
		toret += f'{int(params[1][1]):03b}'
		toret += f'{int(params[2][1:]):08b}'

	elif ctg == 'C':
		toret += f'{opc:05b}'
		toret += f'{0:05b}'
		toret += f'{int(params[1][1]):03b}'
		try:
			toret += f'{int(params[2][1]):03b}'
		except ValueError:
			toret += f'{7:03b}'

	elif ctg == 'D':
		toret += f'{opc:05b}'
		toret += f'{int(params[1][1]):03b}'
		toret += f'{mem.var_addr(params[2]):08b}'

	elif ctg == 'E':
		toret += f'{opc:05b}'
		toret += f'{0:03b}'
		toret += f'{mem.label_addr(params[1]):08b}'
		
	elif ctg == 'F':
		toret += f'{opc:05b}'
		toret += f'{0:011b}'

	return toret