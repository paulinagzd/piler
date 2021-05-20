from symbolTable import SymbolTable
from quad import Quad
import quadHelpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

def incrementParamCounter(cont):
    listLen = len(symbolTable.getCurrentScope().getCurrentFunctionParams())
    if cont > listLen:
      raise Exception("ERROR! function {} called {} arguments, has {}".format(symbolTable.getCurrentScope().getLatestFuncName(), cont, listLen))
    
    print('CURRCONT WILL INCREASE: ', cont)
    cont += 1 
    return cont
  

def verifyParamMatch(cont):
  incoming = quadruple.pilaO.pop()
  incoming_type = quadHelpers.getTypeIfVariable(incoming)
  original = symbolTable.getCurrentScope().getCurrentFunctionParams()[cont]
  print('INCOMING: ',incoming, 'OG: ',original)
  if incoming_type != original.getVarType():
    raise Exception("ERROR! Parameter mismatch")
  else:
    quadruple.saveQuad('PARAM', incoming, None, cont + 1)
    return cont