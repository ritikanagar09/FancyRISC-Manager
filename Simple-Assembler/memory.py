class Memory():
  "maintains a mock memory for the assembler"
  #mem = 0
  #mem_labels = {}
  #mem_vars = {} 

  def __init__(self, m):
    self.mem = m  # where will the next variable be added
    self.mem_labels = {}  # PC of all labels
    self.mem_vars = {}  # memory address of all variables

  def has_label(self,name):
    "checks if a certain label is present in the memory"
    
    return name in self.mem_labels

  def label_addr(self,name):
    "returns the memory address of a named label"

    if name not in self.mem_labels:
      raise ValueError("check if the label is present in memory before using this function!")

    return self.mem_labels[name]

  def has_var(self,name):
    "checks if a certain variable is present in the memory"

    return name in self.mem_vars

  def var_addr(self,name):
    "returns the memory address of a named variable"

    if name not in self.mem_vars:
      raise ValueError("check if the variable is present in memory before using this function!")

    return self.mem_vars[name]

  def store_label(self,name,PC):
    "stores a label with the PC to which it corresponds"

    self.mem_labels[name] = PC

  def store_var(self,name):
    "stores a variable with the memory location to which it corresponds"

    self.mem_vars[name] = self.mem
    self.mem += 2
