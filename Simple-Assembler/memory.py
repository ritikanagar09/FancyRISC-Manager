class Memory():
  "maintains a mock memory for the assembler"
  #mem = 0
  #mem_labels = {}
  #mem_vars = {} 

  def __init__(self, m):
    self.mem = m
    self.mem_labels = {}
    self.mem_vars = {}

  def store_label(self,name,PC):
    "stores a label with the PC to which it corresponds"

    self.mem_labels[name] = PC

  def store_var(self,name):
    "stores a variable with the memory location to which it corresponds"

    self.mem_vars[name] = self.mem
    self.mem += 2
