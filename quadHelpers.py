from semanticCube import SemanticCube
from symbolTable import SymbolTable
from quad import Quad

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

def getType(operand):
  if isinstance(operand,bool):
    return 'boo'
  elif isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,int):
    return 'int'

def check_multdiv_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '*' or workingStack[-1] == '/':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]

      # if (conditional):
      #   print(operator, left_operand, right_operand)
      symbolTable.getCurrentScope().setLatestType(result_Type)

      if result_Type != 'TYPE MISMATCH':
        if operator == '*':
          tvalue = left_operand * right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '/':
          tvalue = left_operand / right_operand
          quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,tvalue)
      else:
        return result_Type
  else:
    print('ESTE ELSE NO HAY WORKINGSTACK', workingStack)

def check_plusminus_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '+' or workingStack[-1] == '-':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      # print(operator, left_operand, right_operand)
      symbolTable.getCurrentScope().setLatestType(result_Type)

      if result_Type != 'TYPE MISMATCH':
        if operator == '+':
          tvalue = left_operand + right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '-':
          tvalue = left_operand - right_operand
          quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,tvalue)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def check_relational_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    operatorSet = {'>','<','==','!=','>=','<='}
    if workingStack[-1] in operatorSet:
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      symbolTable.getCurrentScope().setLatestType(result_Type)
      
      if result_Type != 'TYPE MISMATCH':
        if operator == '>':
          tvalue = left_operand > right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '<':
          tvalue = left_operand < right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '>=':
          tvalue = left_operand >= right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '<=':
          tvalue = left_operand <= right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '==':
          tvalue = left_operand == right_operand
          quadruple.pilaO.append(tvalue)
        elif operator == '!=':
          tvalue = left_operand != right_operand
          quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,tvalue)
      else:
        return result_Type

def check_and_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '&&':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand) 
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = left_operand and right_operand
        quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,tvalue)
      else:
        return result_Type

def check_or_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '||':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = left_operand or right_operand
        quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,tvalue)
      else:
        return result_Type

def check_asig(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '=':
      left_operand = quadruple.pilaO[-1]
      # print(left_operand)
      left_type = getType(left_operand)
      # print(left_type)

      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      assigning_var = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
      result_Type = assigning_var.getVarType()

      if result_Type == left_type:
        quadruple.pilaO.append(assigning_var)
        quadruple.saveQuad(operator,left_operand, None, assigning_var)
      else:
        raise Exception("ERROR! Type mismatch")
  # print(symbolTable.getCurrentScope().getLatestName())
