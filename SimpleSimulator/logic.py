class LU:
	def add(params):
		"adds two integers"
		return {
			'main': params[0] + params[1],
			'flags': int(f"{int(params[0] + params[1] > 255)}000", base = 2)
		}

	def sub(params):
		"subtracts two integers"
		return {
			'main': params[0] - params[1],
		}
	
	def mul(params):
		"multiply two integers"
		return {
			'main': params[0] * params[1],
			'flags':int(f"{int(params[0] * params[1] > 255)}000", base = 2)
		}
	
	def div(params):
		"divides two integers"
		return {
			'main': params[0] // params[1],
			'alter': params[0] % params[1]
		}

	def xor(params):
		"performs bitwise XOR operation"
		return {
			'main': params[0] ^ params[1],
		}

	def orr(params):
		"performs bitwise OR operation"
		return {
			'main': params[0] | params[1],
		}

	def andr(params):
		"performs bitwise AND operation"
		return {
			'main': params[0] & params[1],
		}

	def notr(params):
		"performs bitwise NOT operation"
		return{
			"main": ~ params[1]
		}

	def cmp(params):
		"compares two integers"
		return {
			'flags': int(
					f"0{int(params[0] < params[1])}{int(params[0] > params[1])}{int(params[0] == params[1])}"
				)
		}

	def movr(params):
		"move from register to register"
		return {
			'main': params[1]
		}

	def ld(params):
		"load from memory to register"
		return {
			'main': params[1]
		}

	def st(params):
		"store register in memory"
		return {
			'main': params[0]
		}

	def movi(params):
		"move immediate to register"
		return {
			'main': params[1]
		}

	def jgt(params):
		"jump if greater than"
		return {
			'main': params[0],
			'branch': int(f'{params[1]:016b}'[-2])
		}

	def hlt(params):
		"stops running code"
		return {}

	switcher = {
		0b00000: add,
		0b00001: sub,
		0b00110: mul,
		0b01010: orr,
		0b00010: movi,
		0b00011: movr,
		0b01100: andr,
		0b01101: notr,
		0b10011: hlt,
		0b01110: cmp
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
		toret = {
			'main'  : 0,
			'alter' : 0,
			'branch': 0,
			'flags' : 0,
		}

		gotten = cls.switcher[opc](params)

		for x in gotten:
			toret[x] = gotten[x]

		return toret
