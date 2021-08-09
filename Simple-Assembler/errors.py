import json

def check_variant(variant, line):  
	"checks if the command is broadly valid for the variant identified"

	found = True
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