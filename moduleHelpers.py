from symbolTable import SymbolTable, Variable
from quad import Quad
import quadHelpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

def incrementParamCounter(cont):
    listLen = len(symbolTable.getCurrentScope().getCurrentFunctionParams())
    if cont > listLen:
      raise Exception("ERROR! function {} called {} arguments, has {}".format(symbolTable.getCurrentScope().getLatestFuncName(), cont, listLen))
    
    cont += 1 
    return cont
  

def verifyParamMatch(cont):
  incoming = quadruple.pilaO.pop()

  incoming_type = quadHelpers.getTypeV2(incoming)
  original = symbolTable.getCurrentScope().getCurrentFunctionParams()[cont]
  if incoming_type != original.getVarType():
    raise Exception("ERROR! Parameter mismatch")
  else:
    quadruple.saveQuad('param', incoming, -1, cont + 1)
    return cont
  
def generateGoSub(isClass, className):
  currentScope = symbolTable.getCurrentScope()
  quadruple.saveQuad('gosub', currentScope.getLatestFuncName(), -1, -1) #initial address
  currentScope.clearCurrentFunctionParams()
  currentScope.setMatchingParams(False)
  keyword = ''
  if isClass:
    funcType = symbolTable.getGlobalScope().getScopeClasses()[className].getScopeFunctions()[currentScope.getLatestFuncName()].getScopeType()
  else:
    if currentScope.getContext() == 'classFunction':
      funcType = symbolTable.getGlobalScope().getScopeClasses()[symbolTable.getStack()].getScopeFunctions()[currentScope.getLatestFuncName()].getScopeType()
    else:
      funcType = symbolTable.getGlobalScope().getScopeFunctions()[currentScope.getLatestFuncName()].getScopeType()
  pointingScope = symbolTable.getGlobalScope()
  # need to point either to global or class memory
  if currentScope.getContext() == 'classFunction':
    pointingScope = symbolTable.getGlobalScope().getScopeClasses()[symbolTable.getStack()]

  if funcType != 'void':
    if currentScope.getScopeType() == 'global':
      keyword = 'global'
    else:
      keyword = 'local'
    tempAddressPointer = pointingScope.memory.memSpace[keyword][funcType]['temp']
    tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
    quadruple.pilaO.append(tempAddress)
    quadruple.saveQuad('=', symbolTable.getCurrentScope().getLatestFuncName(), -1, tempAddress) #temp address
    symbolTable.getCurrentScope().getScopeTemps()[quadHelpers.tempCounter] = (Variable('', funcType, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
    quadHelpers.tempCounter += 1
    tempAddressPointer.setOffset() # TODO, will I need more space? or not
