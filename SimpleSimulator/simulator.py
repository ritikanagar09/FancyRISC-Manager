import sys
from storage import Registry, Memory, Tracer
from logic import LU
from controller import CU
from matplotlib import pyplot as plt
import numpy as np

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
#traces_read = [x for x in traces if x[0] == 'R']
traces_read_x = []
traces_read_y = []
traces_write_x = []
traces_write_y = []
#traces_write = [x for x in traces if x[0] == 'W']
#traces_endline = [x for x in traces if x[0] == 'E']
print(traces)
l = 0
for x in traces:
	if x[0] == 'R':
		traces_read_x.append(l)
		traces_read_y.append(x[1])
	elif x[0] == 'W':
		traces_write_x.append(l)
		traces_write_y.append(x[1])
	else:
		l+=1

#x = np.array(range(len(traces)))
#y = np.array([x[1] for x in traces])
plt.scatter(traces_read_x, traces_read_y, marker = 'x', color = 'b', linewidths=1)
plt.scatter(traces_write_x, traces_write_y, marker = 'x', color = 'r', linewidths=1)
plt.savefig('test.png',dpi = 1200)