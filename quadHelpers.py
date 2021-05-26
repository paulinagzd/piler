from semanticCube import SemanticCube
from symbolTable import SymbolTable
from quad import Quad
import condHelpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()

# return the type of each value, either constant or variable
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
  else:
    getVarType(operand)

def getVarType(operand):      
  # if isinstance(operand, dict):
  return list(operand.values())[0]

# only to verify if its a value or constant, don't need a variable type unlike getType
def isVariable(value):
  # if its a variable
  if str(type(value)) == "<class 'symbolTable.Variable'>":
    return 'var'
  else:
    # otherwise its a constant value
    return getType(value)

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

      symbolTable.getCurrentScope().setLatestType(result_Type)

      if result_Type != 'TYPE MISMATCH':
        tvalue = "t{}".format(quadruple.quadCounter)
        # add a temp needed for this function
        symbolTable.getCurrentScope().getTemps[result_Type] += 1
        symbolTable.getCurrentScope().addTemp(result_Type, tvalue) #memory TODO que valor le asigno aqui
        
        quadruple.pilaO.append({tvalue: result_Type}) # t(temp)
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)

        # Saving the operator code instead of the operator itself
        operCode = Quad.operCodes[operator]
        left_operand_dir = left_operand.getVirtualAddress() if isVariable(left_operand) == 'var' else symbolTable.findConstantVirtualAddress(left_operand)
        right_operand_dir = right_operand.getVirtualAddress() if isVariable(right_operand) == 'var' else symbolTable.findConstVA(right_operand)
        tvalue_dir =
        quadruple.saveQuad(operCode,left_operand_dir,right_operand_dir,{tvalue: result_Type})
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch
    # else:
      # print(workingStack[-1])

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

        operCode = Quad.operCodes[operator]
        quadruple.saveQuad(operCode,left_operand,right_operand,{tvalue: result_Type})
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
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})

        operCode = Quad.operCodes[operator]
        quadruple.saveQuad(operCode,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)

      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

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
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        # tvalue = left_operand and right_operand
        # quadruple.pilaO.append(tvalue)

        operCode = Quad.operCodes[operator]
        quadruple.saveQuad(operCode,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch


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
        tvalue = "t{}".format(quadruple.quadCounter)
        quadruple.pilaO.append({tvalue: result_Type})
        # tvalue = left_operand or right_operand
        # quadruple.pilaO.append(tvalue)

        operCode = Quad.operCodes[operator]
        quadruple.saveQuad(operCode,left_operand,right_operand,{tvalue: result_Type})
        symbolTable.getCurrentScope().setLatestExpValue(result_Type)
      else:
        raise Exception('ERROR! Type Mismatch') #type mismatch

def expression_evaluation(p):
  if not quadruple.pOper or quadruple.pOper[-1] == '=' or quadruple.pOper[-1] == 'print':
    if not quadruple.pOper:
      if p[-2] == 'if' or p[-3] == 'while':
        condHelpers.enterCond()
      else:
        # print(quadruple.pilaO[-1])
        p[0] = quadruple.pilaO[-1]
        # print('EVALUACION EXPRESION:', p[0])
        # print(quadruple.pilaO[-2])
        symbolTable.getCurrentScope().setLatestExpValue(p[0])
    elif quadruple.pOper[-1] == '=':
      right_operand = quadruple.pilaO.pop() # this should be a value
      left_operand = quadruple.pilaO.pop() # this should be an id
      right_type = getType(right_operand)
      left_var = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
      left_type = left_var.getVarType()   
      if right_type == left_type:
        operCode = Quad.operCodes['=']
        quadruple.saveQuad(operCode, right_operand, None ,left_operand)
      quadruple.pOper.pop()
    elif quadruple.pOper[-1] == 'print':
      print_operand = quadruple.pilaO.pop() # this should be the value to print
      operCode = Quad.operCodes['print']
      quadruple.saveQuad(operCode, None, None, print_operand)
    else:
      print("WILLIBOOL?")
      print(p[0])

