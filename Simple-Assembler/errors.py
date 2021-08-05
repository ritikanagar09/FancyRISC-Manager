def check(category, line):  # STUB
  found = True
  errors = ["TESTING ERROR", "ANOTHER TESTING ERROR", "YET ANOTHER TESTING ERROR"]  # Might make this a dictionary
  return (found, errors)  

class Logger():
  log = []
  def __init__(self):
    self.log = []
  
  def log_error(self,error):
    self.log.append(error)

  def get_errors(self):
    print(self.log)