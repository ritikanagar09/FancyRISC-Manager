class Registry:
	def __init__(self):
		"initialises registry which is used by the simulator"
		#  starting values are given only for documentation purposes
		self.PC = 0b0000_0000
		self.FLAGS = 0b0000_0000_0000_0000
		self.regs = [0b0000_0000_0000_0000]*7  # general purpose registers

	def write_reg(self, loc: int, val: int):
		"writes a value to a certain register"
		self.regs[loc] = val

	def read_reg(self, loc: int):
		"reads a value from a certain register"
		if loc == 7:
			return self.FLAGS
		return self.regs[loc]

	def set_flags(self, flags: str):
		"sets the flags register with the given flags"
		self.FLAGS = int(f"{0:012b}{flags}", base = 2)

	def spit_PC(self):
		"gets program counter in a printble format"
		print(f"{self.PC:08b} ", end = '')

	def branch_to(self, loc: int):
		"branches to a named instruction"
		Tracer.log_endline(loc)
		self.PC = loc

	def spit_registry(self):
		"returns the full data within the registry, including flags"
		print(" ".join([f'{x:016b}' for x in (self.regs+[self.FLAGS])]), end = ' \n')

class Tracer:
	"logs memory access traces for bonus question"
	traces = []

	@staticmethod
	def log_read(loc):
		"marks that a memory location was read from"
		Tracer.traces.append(('R',loc))

	@staticmethod
	def log_write(loc):
		"marks that a memory location was written to"
		Tracer.traces.append(('W',loc))

	@staticmethod
	def log_endline(loc: int):
		"marks the end of the line"
		Tracer.traces.append(('E',loc))

	def get_all_traces():
		traces_read_x = []
		traces_read_y = []
		traces_write_x = []
		traces_write_y = []

		l = 0
		for x in Tracer.traces:
			if x[0] == 'R':
				traces_read_x.append(l)
				traces_read_y.append(x[1])
			elif x[0] == 'W':
				traces_write_x.append(l)
				traces_write_y.append(x[1])
			else:
				l+=1

		return {'x':{'read':traces_read_x,'write':traces_write_x},'y':{'read':traces_read_y,'write':traces_write_y}}

class Memory:
	def __init__(self, size: int):
		"initialises memory of the given size"
		self.mem = [0b0000_0000_0000_0000]*size

	def write_loc(self, loc: int, val: int):
		"writes a value at a given memory location"
		Tracer.log_write(loc)
		self.mem[loc] = val

	def read_loc(self, loc: int):
		"reads the value at a given memory location"
		Tracer.log_read(loc)
		return self.mem[loc]

	def spit(self):
		"returns the full data within the memory"
		print("\n".join([f'{x:016b}' for x in self.mem])) 