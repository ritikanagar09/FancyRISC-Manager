import sys
from storage import Registry, Memory, Tracer
from logic import LU
from controller import CU
import matplotlib as mpb

lookahead = True
mem = Memory(256)
reg = Registry()

for i,line in enumerate(sys.stdin):
	mem.write_loc(i,int(line, base=2))

while lookahead:
	line = f'{mem.read_loc(reg.PC):016b}'  # open line

	(opc, cat) = CU.interpret(line)  # read type of line and its opcode

	srcs = CU.fetch_sources(cat, line, mem, reg)  # get needed source VALUES
	dests = CU.fetch_destinations(cat, line)  # get needed destination LOCATIONS

	out = LU.call(opc, srcs)  # perform any ALU-related execution needed

	lookahead = CU.store_results(dests, out, opc, cat, mem, reg)  # store results where needed

	reg.spit_PC()  # print PC
	reg.spit_registry()  # print registers values

	CU.next_instruction(out, reg)  # set PC to that of next line

mem.spit()  # print memory once all job is done
traces = Tracer.get_all_traces()  # gets all traces from the tracer