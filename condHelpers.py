from symbolTable import SymbolTable
from quad import Quad, QuadContainer
from jumps import Jumps, TBD
import quadHelpers
import helpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()
jumps = Jumps.instantiate()

def fill(end, cont):
  quadruple.quads[end].setJump(cont)

def enterCond():
  res = quadruple.pilaO.pop()
  resType = helpers.getTypeV2(res)
  if resType != 'boo':
    raise Exception("ERROR! Conditional must have boolean value")
  quadruple.saveQuad('gotoF', res, -1, TBD())
  jumps.setStackPush(quadruple.quadCounter - 1)

def enterElse():
  quadruple.saveQuad('goto', -1, -1, TBD())
  falseValue = jumps.setStackPop()
  jumps.setStackPush(quadruple.quadCounter - 1)
  fill(falseValue, quadruple.quadCounter)

def exitIf():
  end = jumps.setStackPop()
  fill(end, quadruple.quadCounter)

def exitWhile():
  end = jumps.setStackPop()
  ret = jumps.setStackPop()
  quadruple.saveQuad('goto', -1, -1, ret)
  fill(end, quadruple.quadCounter)

def exitDoWhile():
  ret = jumps.setStackPop()
  cond = quadruple.pilaO.pop()
  quadruple.saveQuad('gotoV', cond, -1, ret)

def saveForMain():
  jumps.setStackPush(quadruple.quadCounter)
  quadruple.saveQuad("goto", -1, -1, TBD())

def enterMain():
  ret = jumps.setStackPop() 
  fill(ret, quadruple.quadCounter)
