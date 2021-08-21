class LU:
	def add(params):
		"adds two integers"
		return {
			'main': params[0] + params[1],
			'flags': f"{int(params[0] + params[1] > 255)}000"
		}

	def sub(params):
		"subtracts two integers"
		return {
			'main': params[0] - params[1]
		}

	switcher = {
		0: add,
		1: sub
	}

	@classmethod
	def call(cls, opc: int, params: list) -> dict:
		"""
		calls the function for the given opcode and parameters.

		all parameters are integers in raw form.

		note the purposes of the three output values:
			- main value will contain the main output, which will be stored in a registry.
			- alter value will contain either a second output value [only for div instruction].
			- branch value will contain whether or not to follow branch instruction.
			- flags value will contain the new value of the last 4 bits in the FLAGS register.

		it is to be noted that the alter, branch, and flags values can be merged into one; but they are kept separate for clearer documentation.
		"""
		return {
			'main'  : cls.switcher[opc](params)['main'],
			'alter' : cls.switcher[opc](params)['alter'] or 0,
			'branch': cls.switcher[opc](params)['branch'] or 0,
			'flags' : cls.switcher[opc](params)['flags'] or '0000'
		}
