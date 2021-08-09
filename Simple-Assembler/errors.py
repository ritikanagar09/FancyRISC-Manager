import json

def check_variant(variant, line, PC):  
	"checks if the command is broadly valid for the variant identified"

	"""
	Look up f-strings and split function in python! They will be helpful here. 

	PC can be ignored outside of variable definition statements. Blank statements will never call this function so they dont have to be considered
	
	TEST CASES	
		IN - variant = 'variable', line = 'var pX', PC = 1
		OUT - found = True, errors = ['Variable pX defined after start of program']

		IN - variant = 'instruction', line = 'Zadd R1 R2 R2'
		OUT - found = True, errors = ['Invalid Instruction Name: Zadd']

		IN - variant = 'label', line = 'mylabel : add R1 R2 R3'
		OUT - found = True, errors = ['Label mylabel has whitespace before :']
		[Try splitting by ':' character for this]

		IN - variant = 'label', line = 'mylabel : Zadd R1 R2 R3'
		OUT - found = True, errors = ['Label mylabel has whitespace before :', 'Invalid Instruction Name: Zadd']
		^ If you cant think how to do this case then leave it. The part to the right of the : has to be a valid instruction as well

		IN - variant = 'label', line = 'mylabel : hello : world'
		OUT - found = True, errors = ['the ":" symbol cannot be used multiple times in the same line']
		^ do not display any other error if this is seen

		IN - variant = 'instruction', line = 'add R1 R2 R3'
		OUT - found = False, errors = []

		IN - variant = 'variable', line = 'var x', PC = 0
		OUT - found = False, errors = []

		IN - variant = 'label', line = 'mylabel: add R1 R2 R3' 
		OUT - found = False, errors = []
	"""

	found = False
	errors = ["TESTING ERROR", "ANOTHER TESTING ERROR", "YET ANOTHER TESTING ERROR"]  # Might make this a dictionary
	return (found, errors)  

def check_cat(cat, line, mem): 
	"checks if the command is strictly valid for the given category"

	found = True
	errors = ["TESTING ERROR", "ANOTHER TESTING ERROR", "YET ANOTHER TESTING ERROR"]  # Might make this a dictionary
	return (found, errors)  

class Logger():
	"handles logging of errors in the code"

	log = []
	def __init__(self):
		self.log = []
	
	def log_error(self,lnum,errors):
		"adds an error to the log"
		msg = f"ERROR/S spotted on Line {lnum}\n"
		for error in errors:
			msg += f"{error}\n"
		self.log.append(msg)

	def get_errors(self):
		"gets all errors in the log"

		return self.log
