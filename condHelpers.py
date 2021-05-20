from symbolTable import SymbolTable
from quad import Quad, QuadContainer
from jumps import Jumps, TBD

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()
jumps = Jumps.instantiate()

def fill(end, cont):
  quadruple.quads[end].setJump(cont)

def enterCond():
  if symbolTable.getCurrentScope().getLatestType() != 'boo':
    raise Exception("ERROR! Conditional must have boolean value")
  else:
    res = quadruple.pilaO.pop()
    quadruple.saveQuad('gotoF', res, None, TBD())
    jumps.setStackPush(quadruple.quadCounter - 1)

def enterElse():
  quadruple.saveQuad('goto', None, None, TBD())
  falseValue = jumps.setStackPop()
  jumps.setStackPush(quadruple.quadCounter - 1)
  fill(falseValue, quadruple.quadCounter)

def exitIf():
  end = jumps.setStackPop()
  fill(end, quadruple.quadCounter)

def exitWhile():
  end = jumps.setStackPop()
  ret = jumps.setStackPop()
  quadruple.saveQuad('goto', None, None, ret)
  fill(end, quadruple.quadCounter)

def saveForMain():
  jumps.setStackPush(quadruple.quadCounter)
  quadruple.saveQuad("GOTO", None, None, TBD())

def enterMain():
  ret = jumps.setStackPop() 
  fill(ret, quadruple.quadCounter)
