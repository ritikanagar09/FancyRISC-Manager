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

	def jmp(params):
		"jumps to memory address."
		return {
			'main': params[0],
			'branch': int(f'{params[1]:016b}'[0])
		}

	def jgt(params):
		"jumps to memory address if the greater than flag is set"
		return {
			'main': params[0],
			'branch': int(f'{params[1]:016b}'[-2])
		}

	def jlt(params):
		"jumps to memory address if the less than flag is set"
		return{
			'main':params[0],
			'branch': int(f'{params[1]:016b}'[-3])
			
		}

	def je(params):
		"jumps to memory address if the equal flag is set"
		return{
			'main':params[0],
			'branch': int(f'{params[1]:016b}'[-1])
			
		}
	def div(params):
		"divides two integers"
		return {
			'main': params[0] // params[1],
			'alter': params[0] % params[1]
		}
	
	def cmp(params):
		"compares two integers"
		return {
			'flags': int(
					f"0{int(params[0] < params[1])}{int(params[0] > params[1])}{int(params[0] == params[1])}"
				)
		}

	def rs(params):
		"right shifts register by an immediate value."
		return {
			'main': params[0] >> params[1]
		}
	
	def ls(params):
		"left shifts register by an immediate value"
		return{
			'main':params[0] << params[1]
		}
		

	def hlt(params):
		"stops running code"
		return {}

	switcher = {
		0b00000: add,
		0b00001: sub,
		0b00010: movi,
		0b00011: movr,
		0b00100: ld,
		0b00101: st,
		0b00110: mul,
		0b00111: div, 
		0b01000: rs, 
		0b01001: ls,
		0b01010: xor,
		0b01011: orr,
		0b01100: andr,
		0b01101: notr,
		0b01110: cmp,
		0b01111: jmp,
		0b10000: jlt,
		0b10001: jgt,
		0b10010: je,
		0b10011: hlt,
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
