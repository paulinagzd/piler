def getTypeV2(operand):
  if isinstance(operand, list):
    operand = operand[0]
  if operand >= 5000 and operand < 6999:
    return 'int'
  elif operand >= 7000 and operand < 8999:
    return 'int'
  elif operand >= 9000 and operand < 10999:
    return 'flt'
  elif operand >= 11000 and operand < 12999:
    return 'flt'
  elif operand >= 13000 and operand < 14999:
    return 'cha'
  elif operand >= 15000 and operand < 16999:
    return 'cha'
  elif operand >= 17000 and operand < 18999:
    return 'boo'
  elif operand >= 19000 and operand < 20999:
    return 'boo'
  elif operand >= 21000 and operand < 22999:
    return 'str'
  elif operand >= 23000 and operand < 24999:
    return 'str'
  elif operand >= 25000 and operand < 26999:
    return 'int'
  elif operand >= 27000 and operand < 28999:
    return 'int'
  elif operand >= 29000 and operand < 30999:
    return 'flt'
  elif operand >= 31000 and operand < 32999:
    return 'flt'
  elif operand >= 33000 and operand < 34999:
    return 'cha'
  elif operand >= 35000 and operand < 36999:
    return 'cha'
  elif operand >= 37000 and operand < 38999:
    return 'boo'
  elif operand >= 39000 and operand < 40999:
    return 'boo'
  elif operand >= 41000 and operand < 42999:
    return 'str'
  elif operand >= 43000 and operand < 44999:
    return 'str' 
  elif operand >= 45000 and operand < 46999:
    return 'int'
  elif operand >= 47000 and operand < 48999:
    return 'flt'
  elif operand >= 49000 and operand < 50999:
    return 'cha'
  elif operand >= 51000 and operand < 52999:
    return 'boo'
  elif operand >= 53000 and operand < 54999:
    return 'str'
  elif operand < 5000 or operand >= 55000:
    raise Exception("ERROR! Memory out of bounds")

# return the type of each value, either constant or variable
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
