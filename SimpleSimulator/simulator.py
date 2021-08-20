import sys
from storage import Registry, Memory
from logic import LU
from operator import itemgetter
from controller import CU

lookahead = True
mem = Memory(256)
reg = Registry()

for i,line in enumerate(sys.stdin):
	mem.write_loc(i,line)

while lookahead:
	line = mem.read_loc(reg.PC)
	opcode, params = itemgetter('opcode', 'source')(CU.fetch_params(line))

	out = LU.call(opcode, params)
	CU.handle(opcode, out, mem, reg)

	print(f'{reg.PC:08b} ')
	reg.spit()
	reg.PC += 1 # TODO - deal with branching shenanigans

mem.spit()