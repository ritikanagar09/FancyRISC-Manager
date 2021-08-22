import json
from storage import Memory, Registry

class CU:
	@staticmethod
	def get_opcode(line):
		"returns the opcode of a line"
		return int(line[0:5], base=2)

	insts = json.load(open('../Simple-Assembler/instructions.json'))
	@classmethod
	def get_type_from_opcode(cls, opc: int) -> str:
		"returns the type of the command from its opcode"
		for inst in cls.insts:  # Iterates through each instruction name
			for form in inst:  # Iterates through forms of each instruction
				if form['opcode'].endswith(f'{opc:05b}'):
					return form['type']

	@classmethod
	def interpret(cls, line):
		opc = cls.get_opcode(line)
		return (opc,cls.get_type_from_opcode(opc))

	@classmethod
	def fetch_sources(cls, opc, cat, line, mem: Memory, reg: Registry) -> dict:
		"gets the values used as source operand/s by a line of code, along with opcode and category"

		sources = [] # TODO: Get these according to category

		"""
		To read value in a register location:
			-> reg.read_reg(int('001', base = 2)),
		
		To read value in a memory location:
		  -> mem.read_loc(int('00100010', base = 2))

		To read an immediate:
		  -> int('00100010', base = 2)
		"""

		if cat == 'A':
			sources = [
				reg.read_reg(int(line[10:13], base = 2)),
				reg.read_reg(int(line[13:], base = 2))
			]

		elif cat=='B':
			sources = [
			reg.read_reg(int(line[5:8], base = 2)),
			int(line[8:], base = 2)
			]
			
		elif cat=='C':
			sources = [
				reg.read_reg(int(line[10:13], base = 2)),
				reg.read_reg(int(line[13:], base = 2))
		]	
		elif cat=='D':
			sources = [
				reg.read_reg(int(line[5:8], base = 2)),
				mem.read_loc(int(line[8:], base = 2))
			]
			
		elif cat=='E':
			sources = [
				mem.read_loc(int(line[8:], base = 2))
			]
			
		elif cat=='F':
			sources = []

		return sources
	

	@staticmethod
	def fetch_destinations(cat: int, line: str) -> list:
		"gets the values used as destination operand/s by a line of code"
		
		if cat == 'A':
			dests = [
				int(line[7:10], base = 2)
			]
		
		elif cat == 'B':
			dests = [
				int(line[5:8], base = 2)
			]
			
		elif cat == 'C':
			dests = [
				int(line[10:13], base = 2),
				int(line[13:], base = 2)
			]
		
		elif cat == 'D':
			dests = [
				int(line[5:8], base = 2),
				int(line[8:], base = 2)
			]

		elif cat == 'E':
			dests = []

		elif cat == 'F':
			dests = []

		return dests
	
	@staticmethod
	def store_results(dests, output, opc: int, cat: str, mem: Memory, reg: Registry) -> bool:
		"handles output after execution is done. returns whether or not there are lines afterwards."

		reg.FLAGS = 0b0000_0000_0000_0000

		if cat == 'F':
			return False

		elif cat == 'D':
			if opc & 1:
				mem.write_loc(dests[0], output['main'])
			else:
				reg.write_reg(dests[0], output['main'])

		elif cat == 'C':
			if opc in (0b00011, 0b01101) :  # mov / not
				reg.write_reg(dests[0], output['main'])

			elif opc == 0b00111:  # div
				reg.write_reg(dests[0], output['main'])
				reg.write_reg(dests[1], output['alter'])

			elif opc == 0b01110:  # cmp
				reg.set_flags(output['flags'])

		elif cat in ('B','A'):
			reg.write_reg(dests[0], output['main'])

		return True

	@staticmethod
	def next_instruction(output, reg: Registry):
		"branches to next instruction of PC, and returns False if stopping is required"

		if output['branch']:
			reg.branch_to(output['main'])
		else:
			reg.branch_to(reg.PC+1)
