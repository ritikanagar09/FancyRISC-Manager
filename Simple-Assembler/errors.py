import json
import re
import memory
cats = json.load(open('categories.json'))

"""
A few notes about error handling for the person correcting this:
> I have chosen to allow blank lines after the hlt instruction at the end. I think   	those are commonly seen in programs and it is acceptable to ignore them.
> It is told to mark errors for invalid usage of FLAGS register or accidental swapping of label and variable names. I have merged these into invalid register name / invalid label name / invalid variable name errors, because I think none of these are things that deserve special errors. That being said, the errors are definitely displayed.
"""

def check_variant(variant, line, PC):  
	"checks if the command is broadly valid for the variant identified"

	# Default return values
	found = False
	errors = []

	if variant == 'label':
		if line.count(':') >= 2:
			found = True
			errors.append('the ":" symbol cannot be used multiple times in the same line')
		if line[line.index(':')-1]==' ':
			found = True
			errors.append('Label has whitespace before :')
	if variant == 'variable':
		if PC>0:
			found = True
			errors.append('Variable defined after start of program')
	if variant == 'instruction':
		params = line.split()	
		if len(params) == 0 or params[0] not in insts:  		# if invalid instruction category
			found = True
			errors.append('Instruction missing or unidentified')
		return (found, errors)
		insts = json.load(open('instructions.json'))
	
	"""
	Look up f-strings and split function in python! They will be helpful here. 

	PC can be ignored outside of variable definition statements. Blank statements will never call this function so they dont have to be considered
	
	TEST CASES	
		IN - variant = 'variable', line = 'var pX', PC = 1
		OUT - found = True, errors = ['Variable defined after start of program']

		IN - variant = 'instruction', line = 'Zadd R1 R2 R2'
		OUT - found = True, errors = ['Invalid Instruction Name']

		IN - variant = 'label', line = 'mylabel : add R1 R2 R3'
		OUT - found = True, errors = ['Label has whitespace before :']
		[Try splitting by ':' character for this]

		IN - variant = 'label', line = 'mylabel : Zadd R1 R2 R3'
		OUT - found = True, errors = ['Label mylabel has whitespace before :', 'Invalid Instruction Name: Zadd']
		^ If you cant think how to do this case then leave it. The part to the right of the : has to be a valid instruction as well

		IMPORTANT - This test case is implemented in the code above!! => IN - variant = 'label', line = 'mylabel : hello : world' 
		OUT - found = True, errors = ['the ":" symbol cannot be used multiple times in the same line']
		^ do not display any other error if this is seen

		IN - variant = 'instruction', line = 'add R1 R2 R3'
		OUT - found = False, errors = []

		IN - variant = 'variable', line = 'var x', PC = 0
		OUT - found = False, errors = []

		IN - variant = 'label', line = 'mylabel: add R1 R2 R3' 
		OUT - found = False, errors = []
	"""

	#found = False
	#errors = ["TESTING ERROR", "ANOTHER TESTING ERROR", "YET ANOTHER TESTING ERROR"]  # Might make this a dictionary
	return (found, errors)  

regnames = re.compile('R[0-6]')
def invalid_registers(regs):
	"returns the invalid registers from a list of register names"
	return [x for x in regs if not regnames.fullmatch(x)]

def invalid_imm(imm: str):
	"returns invalidity and issue in an immediate"
	if not imm[0] == '$':
		return (True,"immediate name must start with '$' symbol")
	if not imm[1:].isdigit():
		return (True,f"{imm} is not a positive integer")
	elif int(imm) > 255 or int(imm) < 0:
		return (True,f"{imm} lies beyond the integer size limit")
	return (False)
	
def check_cat(cat, line, mem: memory.Memory,lookahead): 
	"checks if the command is strictly valid for the given category"

	params = line.split()
	errors = []

	if cat == 'unidentified':
		errors.append(f"instruction {params[0]} not identified")
		return (True, errors)

	l = len(params)
	l0 = len([x for x in cats[cat]['encoding'] if x != "unused"])
	if l0 != l:
		errors.append(f"{l-1} parameter/s given, but the {params[0]} instruction expects {l0-1}")

	if cat == 'A' or cat == 'C':
		try:
			if len(params) >= 1:
				if len(invalid_registers(params[1:])) > 0:
					errors.extend([f"invalid register name: {x}" for x in invalid_registers(params[1:])])
		except:
			pass
	
	elif cat == 'B':
		try:
			if len(invalid_registers([params[1]])) > 0:
				errors.extend([f"invalid register name: {x}" for x in invalid_registers([params[1]])])

			if invalid_imm(params[2])[0]:
				errors.append(invalid_imm(params[2])[1])
		except:
			pass
	
	elif cat == 'D':
		try:
			if len(invalid_registers([params[1]])) > 0:
				errors.extend([f"invalid register name: {x}" for x in invalid_registers([params[1]])])

			if not mem.has_var(params[2]):
				errors.append(f"invalid variable name: {params[2]}")
		except:
			pass
	
	elif cat == 'E':
		try:
			if not mem.has_label(params[1]):
				errors.append(f"invalid label name: {params[1]}")
		except:
			pass
		
	elif cat == 'F':
		if lookahead:
			errors.append('hlt instruction used before end of program.')
	
	if not lookahead and cat != 'F':
		errors.append('hlt instruction not found on last line of program.')

	found = len(errors) != 0
	return (found, errors)  

class Logger():
	"handles logging of errors in the code"

	log = []
	def __init__(self):
		self.log = []

	def errors_present(self):
		"checks if there are any errors in the log"

		return len(self.log) > 0

	def log_error(self,lnum,errors):
		"adds an error to the log"

		msg = f"ERROR/S spotted on Line {lnum}\n"
		for error in errors:
			msg += f"{error}\n"
		self.log.append(msg)

	def get_errors(self):
		"gets all errors in the log"

		return self.log
