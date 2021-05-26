from semanticCube import SemanticCube
from symbolTable import SymbolTable
from quad import Quad
import condHelpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

varPointer = None

def getType(operand):
  if operand == 'True' or operand == 'False':
    return 'boo'
  elif isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,int):
    return 'int'
  elif isinstance(operand, str):
    if len(operand) == 3 and operand[0] == '\'':
      return 'cha'
    else:
      return 'str'
  elif isinstance(operand, dict):
    return list(operand.values())[0]

def getTypeIfVariable(operand):
  if str(type(operand)) == "<class 'symbolTable.Variable'>":
    return operand.getVarType()
  else:
    return getType(operand)
     
def check_multdiv_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '*' or workingStack[-1] == '/':
      right_operand = quadruple.pilaO.pop() 
      right_type = getTypeIfVariable(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getTypeIfVariable(left_operand)
      print("TYPEEEEEEE", left_operand, right_operand)

      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]

      symbolTable.getCurrentScope().setLatestType(result_Type)

      if result_Type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)
        # if operator == '*':
        #   tvalue = left_operand * right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '/':
        #   tvalue = left_operand / right_operand
        #   quadruple.pilaO.append(tvalue)


        # Saving the operator code instead of the operator itself
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch
    # else:
      # print(workingStack[-1])

def check_plusminus_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '+' or workingStack[-1] == '-':
      right_operand = quadruple.pilaO.pop() 
      right_type = getTypeIfVariable(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getTypeIfVariable(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      symbolTable.getCurrentScope().setLatestType(result_Type)

      if result_Type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)

        # if operator == '+':
        #   tvalue = left_operand + right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '-':
        #   tvalue = left_operand - right_operand
        #   quadruple.pilaO.append(tvalue)

        
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_relational_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    operatorSet = {'>','<','==','!=','>=','<='}
    if workingStack[-1] in operatorSet:
      right_operand = quadruple.pilaO.pop() 
      right_type = getTypeIfVariable(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getTypeIfVariable(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      symbolTable.getCurrentScope().setLatestType(result_Type)
      
      if result_Type != 'TYPE MISMATCH':
        # if operator == '>':
        #   tvalue = left_operand > right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '<':
        #   tvalue = left_operand < right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '>=':
        #   tvalue = left_operand >= right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '<=':
        #   tvalue = left_operand <= right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '==':
        #   tvalue = left_operand == right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '!=':
        #   tvalue = left_operand != right_operand
        #   quadruple.pilaO.append(tvalue)
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)

      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_and_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '&&':
      right_operand = quadruple.pilaO.pop()
      right_type = getTypeIfVariable(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getTypeIfVariable(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        # tvalue = left_operand and right_operand
        # quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch


def check_or_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '||':
      right_operand = quadruple.pilaO.pop()
      right_type = getTypeIfVariable(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getTypeIfVariable(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        # tvalue = left_operand or right_operand
        # quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def expression_evaluation(p):
  if not quadruple.pOper or quadruple.pOper[-1] == '=' or quadruple.pOper[-1] == 'print':
    if not quadruple.pOper:
      if p[-2] == 'if' or p[-3] == 'while':
        condHelpers.enterCond()
      else:
        p[0] = quadruple.pilaO[-1]
        symbolTable.getCurrentScope().setLatestExpValue(p[0])
    elif quadruple.pOper[-1] == '=':
      right_operand = quadruple.pilaO.pop() # this should be a value
      while str(type(quadruple.pilaO[-1])) != "<class 'symbolTable.Variable'>":
        quadruple.pilaO.pop()
      left_operand = quadruple.pilaO.pop() # this should be an id
      right_type = getType(right_operand)
      left_var = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
      left_type = left_var.getVarType()      
      if right_type == left_type:
        quadruple.saveQuad('=', right_operand, None ,left_operand)
      quadruple.pOper.pop()
    elif quadruple.pOper[-1] == 'print':
      print_operand = quadruple.pilaO.pop() # this should be the value to print
      quadruple.saveQuad('print', None, None, print_operand)
  elif quadruple.pOper[-1] == '[':
    lsPointer = quadruple.pilaDim[-1]["id"].getDimensionNodes()
    currentDim = quadruple.pilaDim[-1]["dim"]
    quadruple.saveQuad("verify", quadruple.pilaO[-1], 0, lsPointer[currentDim-1].getLim()) # -1 because array index
    tvalue = "t{}".format(quadruple.quadCounter)
    if symbolTable.getCurrentScope().getLatestDimension() > 1: # TODO
    # print("POR QUE ES J", quadruple.pilaO[-1])
        aux = quadruple.pilaO.pop()
        quadruple.saveQuad("*", aux, lsPointer[currentDim-1].getR(), {tvalue: 'int'})
        quadruple.pilaO.append({tvalue: 'int'})
    if currentDim > 1:
      left_operand = quadruple.pilaO.pop()
      right_operand = quadruple.pilaO.pop()
      quadruple.saveQuad("+", left_operand, right_operand, tvalue)
      quadruple.pilaO.append({tvalue: 'int'})

def dimensionQuad(current, currDim):
  print("CURR DIM IS", currDim)
  global varPointer
  if currDim == 1:
    idVar = quadruple.pilaO.pop()
    varPointer = current.verifyDim(idVar)
    quadruple.pilaDim.append({"id": varPointer, "dim": currDim})
    dimNode = varPointer.getDimensionNodes()
    quadruple.pOper.append('[') # fakeBottom
  else:
    quadruple.pilaDim.pop()
    quadruple.pilaDim.append({"id": varPointer, "dim": current.getLatestDimension()})

def endDim():
  print("ENTER ENDDIM")
  tvalue = "t{}".format(quadruple.quadCounter)
  current = symbolTable.getCurrentScope()
  aux = quadruple.pilaO.pop()
  global varPointer
  varPointerDimNodes = varPointer.getDimensionNodes()
  # if current.getLatestDimension() == 1:
  #   print(current.getLatestDimension()) # se supone que en mi primera direccion
  quadruple.saveQuad("+", aux, varPointerDimNodes[current.getLatestDimension()-1].getR(), {tvalue: 'int'}) # ojo offset for first ones
  # else:
  #   # print("DIMENSION LOCA", current.getLatestDimension())
  #   quadruple.saveQuad("+", aux, 0, tvalue) # ojo offset for first ones
  quadruple.saveQuad("+", {"id": "t{}".format(quadruple.quadCounter - 1), "varType": 'int'}, varPointer.getVirtualAddress(), {"t{}".format(quadruple.quadCounter+1), 'int'})
  quadruple.pilaO.append(tvalue) # to change to address
  quadruple.pOper.pop() # eliminates fake bottom
  current.resetLatestDimension()

