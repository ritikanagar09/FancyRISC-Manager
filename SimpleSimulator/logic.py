class LU:
	def add(params):
		"adds two integers"
		# TODO - handle overflow.. somewhere
		return params[0] + params[1]

	def sub(params):
		"subtracts two integers"
		return params[0] - params[1]

	switcher = {
		0: add,
		1: sub
	}

	@classmethod
	def call(cls, opc: int, params: list):
		"calls the function for the given opcode and parameters"
		return cls.switcher[opc](params)

print(LU.call(0,[1,2]))