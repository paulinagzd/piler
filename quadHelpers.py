from semanticCube import SemanticCube
from symbolTable import SymbolTable, Variable
from quad import Quad
import condHelpers
import helpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

varPointer = None
tempCounter = 0

def getPointingScope(currentScope):
  # need to point either to global or class memory
  if currentScope.getContext() == 'classFunction':
    return symbolTable.getGlobalScope().getScopeClasses()[symbolTable.getStack()]
  else:
    return symbolTable.getGlobalScope()
     
def check_multdiv_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '*' or workingStack[-1] == '/':
      right_operand = quadruple.pilaO.pop() 
      right_type = helpers.getTypeV2(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = helpers.getTypeV2(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_type = SemanticCube[operator][left_type][right_type]

      symbolTable.getCurrentScope().setLatestType(result_type)

      if result_type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)

        # get next temp memory depending on type
        keyword = ''
        if symbolTable.getCurrentScope().getContext() == 'global':
          keyword = 'global'
        else:
          keyword = 'local'
        tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][result_type]['temp']
        tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
        quadruple.pilaO.append(tempAddress)
        symbolTable.getCurrentScope().setLatestExpValue(result_type)
        quadruple.saveQuad(operator,left_operand,right_operand, tempAddress)
        global tempCounter
        symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', result_type, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
        tempCounter += 1
        tempAddressPointer.setOffset()
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_plusminus_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '+' or workingStack[-1] == '-':
      right_operand = quadruple.pilaO.pop() 
      right_type = helpers.getTypeV2(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = helpers.getTypeV2(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_type = SemanticCube[operator][left_type][right_type]
      symbolTable.getCurrentScope().setLatestType(result_type)

      if result_type != 'TYPE MISMATCH':
        # get next temp memory depending on type
        keyword = ''
        if symbolTable.getCurrentScope().getContext() == 'global':
          keyword = 'global'
        else:
          keyword = 'local'
        tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][result_type]['temp']
        tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
        quadruple.pilaO.append(tempAddress)
        symbolTable.getCurrentScope().setLatestExpValue(result_type)
        quadruple.saveQuad(operator,left_operand,right_operand, tempAddress)
        global tempCounter
        symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', result_type, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
        tempCounter += 1        
        tempAddressPointer.setOffset()
        
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_relational_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    operatorSet = {'>','<','==','!=','>=','<='}
    if workingStack[-1] in operatorSet:
      right_operand = quadruple.pilaO.pop() 
      left_operand = quadruple.pilaO.pop()
      right_type = helpers.getTypeV2(right_operand)
      left_type = helpers.getTypeV2(left_operand)

      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_type = SemanticCube[operator][left_type][right_type]
      symbolTable.getCurrentScope().setLatestType(result_type)
      
      if result_type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        # get next temp memory depending on type
        keyword = ''
        if symbolTable.getCurrentScope().getContext() == 'global':
          keyword = 'global'
        else:
          keyword = 'local'
        tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][result_type]['temp']
        tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
        quadruple.pilaO.append(tempAddress)
        tempAddressPointer.setOffset()
        quadruple.saveQuad(operator,left_operand,right_operand,tempAddress)
        global tempCounter
        symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', result_type, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
        tempCounter += 1
        symbolTable.getCurrentScope().setLatestExpValue(result_type)

      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_and_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '&&':
      right_operand = quadruple.pilaO.pop()
      right_type = helpers.getTypeV2(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = helpers.getTypeV2(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_type = SemanticCube[operator][left_type][right_type]
      
      if result_type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        # get next temp memory depending on type
        keyword = ''
        if symbolTable.getCurrentScope().getContext() == 'global':
          keyword = 'global'
        else:
          keyword = 'local'

        tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][result_type]['temp']
        tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
        quadruple.pilaO.append(tempAddress)
        quadruple.saveQuad(operator,left_operand,right_operand, tempAddress)
        global tempCounter
        symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', result_type, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
        tempCounter += 1        
        tempAddressPointer.setOffset()
        symbolTable.getCurrentScope().setLatestExpValue(result_type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch


def check_or_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '||':
      right_operand = quadruple.pilaO.pop()
      right_type = helpers.getTypeV2(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = helpers.getTypeV2(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_type = SemanticCube[operator][left_type][right_type]
      
      if result_type != 'TYPE MISMATCH':
        # get next temp memory depending on type
        keyword = ''
        if symbolTable.getCurrentScope().getContext() == 'global':
          keyword = 'global'
        else:
          keyword = 'local'
        tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][result_type]['temp']
        tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
        quadruple.pilaO.append(tempAddress)
        quadruple.saveQuad(operator,left_operand,right_operand, tempAddress)
        global tempCounter
        symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', result_type, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
        tempCounter += 1  
        tempAddressPointer.setOffset()

        symbolTable.getCurrentScope().setLatestExpValue(result_type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def expression_evaluation(p):
  if not quadruple.pOper or quadruple.pOper[-1] == '=' or quadruple.pOper[-1] == 'print':
    if not quadruple.pOper:
      if p[-2] == 'if' or p[-3] == 'while':
        condHelpers.enterCond()
    elif quadruple.pOper[-1] == '=':
      right_operand = quadruple.pilaO.pop() # this should be a value
      left_operand = quadruple.pilaO.pop() # this should be an id
      right_type = helpers.getTypeV2(right_operand)
      left_type = helpers.getTypeV2(left_operand)   
      if right_type == left_type:
        quadruple.saveQuad('=', right_operand, -1 ,left_operand)
      else:
        raise Exception("ERROR! cannot assign type {} to {}".format(left_type, right_type))
      quadruple.pOper.pop()
    elif quadruple.pOper[-1] == 'print' and not symbolTable.getCurrentScope().getMatchingParams():
      print_operand = quadruple.pilaO.pop() # this should be the value to print
      quadruple.saveQuad('print', -1, -1, print_operand)
  elif quadruple.pOper[-1] == '$':
    lsPointer = quadruple.pilaDim[-1]["id"].getDimensionNodes()
    currentDim = quadruple.pilaDim[-1]["dim"]
    quadruple.saveQuad("verify", quadruple.pilaO[-1], 0, lsPointer[currentDim-1].getLim()) # -1 because array index
    keyword = ''
    if symbolTable.getCurrentScope().getContext() == 'global':
      keyword = 'global'
    else:
      keyword = 'local'
    currType = helpers.getTypeV2(quadruple.pilaO[-1])
    tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][currType]['temp']
    tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
    global tempCounter
    if len(lsPointer) > currentDim: 
      aux = quadruple.pilaO.pop()
      quadruple.saveQuad("*a", aux, lsPointer[currentDim-1].getMDim(), tempAddress)      
      symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', currType, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
      tempCounter += 1        
      quadruple.pilaO.append(tempAddress)
      tempAddressPointer.setOffset()
    if currentDim > 1:
      left_operand = quadruple.pilaO.pop()
      right_operand = quadruple.pilaO.pop()
      print("LR", left_operand, right_operand)
      tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
      quadruple.saveQuad("+", left_operand, right_operand, tempAddress)
      symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', currType, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
      tempCounter += 1        
      quadruple.pilaO.append(tempAddress)
      tempAddressPointer.setOffset()
  elif quadruple.pOper[-1] == 'return':
    if symbolTable.getCurrentScope().getScopeType() == 'void':
      if quadruple.pilaO[-1]:
        raise Exception("ERROR! Void functions cannot return values")

    expValue = quadruple.pilaO.pop()
    expValueType = helpers.getTypeV2(expValue)
    if expValueType != symbolTable.getCurrentScope().getScopeType():
      raise Exception("ERROR! Type mismatch in returning function")
    # if void, return should have no expValue
    quadruple.saveQuad('return', -1, -1, expValue)
    quadruple.pOper.pop()

def endDim(var):
  current = symbolTable.getCurrentScope()
  aux = quadruple.pilaO.pop()
  varPointerDimNodes = var.getDimensionNodes()
  keyword = ''
  if symbolTable.getCurrentScope().getContext() == 'global':
    keyword = 'global'
  else:
    keyword = 'local'
  currType = helpers.getTypeV2(quadruple.pilaO[-1])
  tempAddressPointer = getPointingScope(symbolTable.getCurrentScope()).memory.memSpace[keyword][currType]['temp']
  tempAddress = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
  quadruple.saveQuad("+a", aux, varPointerDimNodes[var.getDimensions()-1].getOffset(), tempAddress)  
  global tempCounter
  symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', currType, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
  tempCounter += 1        
  tempAddressPointer.setOffset()
  tempAddress2 = tempAddressPointer.getInitialAddress() + tempAddressPointer.getOffset()
  quadruple.saveQuad("+a", tempAddress, var.getVirtualAddress(), tempAddress2)

  symbolTable.getCurrentScope().getScopeTemps()[tempCounter] = (Variable('', currType, 0, [], tempAddressPointer.getOffset(), False, tempAddressPointer, False))
  tempCounter += 1        
  quadruple.pilaO.pop() # gets rid of dirBase
  tempAddressPointer.setOffset()
  quadruple.pilaO.append([tempAddress2])
  quadruple.pOper.pop() # eliminates fake bottom
  quadruple.pilaDim.pop()
  current.resetLatestDimension()
  return True
