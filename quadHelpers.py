from semanticCube import SemanticCube
from symbolTable import SymbolTable
from quad import Quad
import condHelpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

def getType(operand):
  if operand == 'True' or operand == 'False':
    return 'boo'
  elif isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,int):
    return 'int'
  elif isinstance(operand, str):
    return 'str'
  elif isinstance(operand, dict):
    return list(operand.values())[0]

def getTypeIfVariable(operand):
  if str(type(operand)) == "<class 'symbolTable.Variable'>":
    return operand.getVarType()
  else:
    return getType(operand)

def expression_evaluation(p):
  if not quadruple.pOper or quadruple.pOper[-1] == '=' or quadruple.pOper[-1] == 'print':
    if not quadruple.pOper:
      if p[-2] == 'if' or p[-3] == 'while':
        condHelpers.enterCond()
      else:
        p[0] = quadruple.pilaO.pop()
        print('EVALUACION EXPRESION:', p[0])
      # symbolTable.getCurrentScope().setLatestExpValue(p[0])
    elif quadruple.pOper[-1] == '=':
      right_operand = quadruple.pilaO.pop() # this should be a value
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

def check_multdiv_operator(quadruple):
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '*' or workingStack[-1] == '/':
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
        # if operator == '*':
        #   tvalue = left_operand * right_operand
        #   quadruple.pilaO.append(tvalue)
        # elif operator == '/':
        #   tvalue = left_operand / right_operand
        #   quadruple.pilaO.append(tvalue)
        quadruple.saveQuad(operator,left_operand,right_operand,{tvalue: result_Type})
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

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
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch


