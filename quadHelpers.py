from semanticCube import SemanticCube
from symbolTable import SymbolTable
from quad import Quad

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

def getType(operand):
  if isinstance(operand,int):
    return 'int'
  elif isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,bool):
    return 'boo'

def check_multdiv_operator(quadruple,workingStack):
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

def check_plusminus_operator(quadruple,workingStack):
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
      print(operator, left_operand, right_operand)
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

def check_relational_operator(quadruple,workingStack):
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

def check_and_operator(quadruple,workingStack):
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

def check_or_operator(quadruple,workingStack):
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