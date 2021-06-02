# getTypeV2
# What: Gets the type of the value depending on the memory address
# Parameters: The value of the address
# Returns the type of the address that's being used
# When is it used: During every type matching call (expressions)
def getTypeV2(operand):
  if isinstance(operand, list):
    operand = operand[0]
  if operand >= 5000 and operand < 8999 or \
     operand >= 25000 and operand < 28999 or \
     operand >= 45000 and operand < 46999:
    return 'int'
  elif operand >= 9000 and operand < 12999 or \
       operand >= 29000 and operand < 32999 or \
       operand >= 47000 and operand < 48999:
    return 'flt'
  elif operand >= 13000 and operand < 16999 or \
       operand >= 33000 and operand < 36999 or \
       operand >= 49000 and operand < 50999:
    return 'cha'
  elif operand >= 17000 and operand < 20999 or \
       operand >= 37000 and operand < 40999 or \
       operand >= 51000 and operand < 52999:
    return 'boo'
  elif operand >= 21000 and operand < 24999 or \
       operand >= 41000 and operand < 44999 or \
       operand >= 53000 and operand < 54999:
    return 'str'
  elif operand < 5000 or operand >= 55000:
    raise Exception("ERROR! Memory out of bounds")

# getTypeConstants
# What: Function to get the type of constant depending of instances
# Parameters: The value of the address
# Returns the type of each value, either constant or variable
# When is it used: During every type matching call with constants (expressions)
def getTypeConstants(operand):
  if isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,int):
    return 'int'
  elif isinstance(operand, str):
    if len(operand) == 3 and operand[0] == '\'':
      return 'cha'
    else:
      return 'str'
