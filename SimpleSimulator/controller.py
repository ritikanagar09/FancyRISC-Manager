import json
from storage import Memory, Registry

class CU:
  @staticmethod
  def get_opcode(line):
    "returns the opcode of a line"
    return int(line[0:5], base=2)

  insts = json.load(open('../Simple-Assembler/instructions.json'))
  @classmethod
  def get_type_from_opcode(cls, opc: int):
    "returns the type of the command from its opcode"
    for inst in cls.insts:  # Iterates through each instruction name
      for form in inst:  # Iterates through forms of each instruction
        if form['opcode'].endswith(f'{opc:05b}'):
          return form['type']
  
  @classmethod
  def fetch_params(cls, line, mem: Memory, reg: Registry):
    "gets the values used as LHS operands by a line of code"

    # Split function into interpret and read functions maybe?

    opc = cls.get_opcode(line)
    cat = cls.get_type_from_opcode(opc)

    if cat == 'A':
      return {
        'opcode': opc,
        'source': [
          reg.read_reg(int(line[10:13], base = 2)), 
          reg.read_reg(int(line[13:16], base = 2))
        ]
      }


  @classmethod
  def handle(cls, opc: int, mem: Memory, reg: Registry):
    if opc >= 0b10000:
      "This is a branching instruction"
    reg.write_reg()