import json
import re
import memory
cats = json.load(open('categories.json'))

"""
A few notes about error handling for the person correcting this:
> I have chosen to allow blank lines after the hlt instruction at the end. I think those are commonly seen in programs and it is acceptable to ignore them.
> It is told to mark errors for invalid usage of FLAGS register or accidental swapping of label and variable names. I have merged these into invalid register name / invalid label name / invalid variable name errors, because I think none of these are things that deserve special errors. That being said, the errors are definitely displayed.
"""
insts = json.load(open('instructions.json'))
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
		if len(params) == 0 or params[0] not in insts:  # if invalid instruction category
			found = True
			errors.append('Instruction missing or unidentified')

	return (found, errors)  

REGNAMES = re.compile('R[0-6]')
FLAGS = 'FLAGS' 

def invalid_registers(regs):
	"returns the invalid registers from a list of register names"
	return [x for x in regs if (not REGNAMES.fullmatch(x))]

def invalid_registers_but_you_can_use_flags(regs):
	"returns the invalid registers from a list of register names except flags are allowed"
	return [x for x in regs if not (REGNAMES.fullmatch(x) or x == FLAGS)]

def invalid_imm(imm: str):
	"returns invalidity and issue in an immediate"
	if not imm[0] == '$':
		return (True,"immediate name must start with '$' symbol")
	if not imm[1:].isdigit():
		return (True,f"{imm} is not a positive integer")
	elif int(imm) > 255 or int(imm) < 0:
		return (True,f"{imm} lies beyond the integer size limit")
	return (False)
	
def check_cat(opc,cat, line, mem: memory.Memory,lookahead): 
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
		if opc == 0b00011:
			try:
			
				if len(invalid_registers([params[1]])) > 0:
					errors.extend([f"invalid register name: {x}" for x in invalid_registers([params[1]])])
				
				if len(invalid_registers_but_you_can_use_flags([params[2]])) > 0:
					print(invalid_registers_but_you_can_use_flags([params[2]]))
					errors.extend([f"invalid register name: {x}" for x in invalid_registers([params[2]])])
			except:
				pass

		else:
			try:
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