class Registry:
  def __init__(self):
    self.PC = 0
    self.regs = [0]*7

  def write_loc(self, loc: int, val: int):
    self.regs[loc] = val

  def read_loc(self, loc: int):
    return self.regs[loc]

  def spit(self):
    return " ".join(self.regs)

class Memory:
  def __init__(self, size: int):
    self.mem = [0]*size

  def write_loc(self, loc: int, val: int):
    self.mem[loc] = val

  def read_loc(self, loc: int):
    return self.mem[loc]

  def spit(self):
    return "\n".join(self.mem)
  
  