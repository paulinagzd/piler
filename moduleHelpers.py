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
  print('INCOMING: ',incoming, incoming_type, 'ORIGINAL PARAM: ',original)
  if incoming_type != original.getVarType():
    raise Exception("ERROR! Parameter mismatch")
  else:
    quadruple.saveQuad('param', incoming, None, cont + 1)
    return cont
  

# def endingFunction():
#   print("ENDING FUNCTION")
#   print(symbolTable.getCurrentScope().getScopeName(), symbolTable.getCurrentScope().getLatestExpValue())
#   if symbolTable.getCurrentScope().getScopeType() != symbolTable.getCurrentScope().getLatestExpValue():
#     raise Exception('ERROR!', symbolTable.getCurrentScope().getScopeName(), 'function must return  value of type', symbolTable.getCurrentScope().getScopeType())
#   else:
#     quadruple.saveQuad("endfunc", None, None, None)
