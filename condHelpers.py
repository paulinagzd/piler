from symbolTable import SymbolTable
from quad import Quad, QuadContainer
from jumps import Jumps, TBD
import quadHelpers
import helpers

quadruple = Quad.instantiate()
symbolTable = SymbolTable.instantiate()
jumps = Jumps.instantiate()

# Helper to modify quadruple's pending jump
def fill(end, cont):
  quadruple.quads[end].setJump(cont)

# enterCond
# What: Saves quad and sets jump when it enters a condition
# When is it used: Everytime a conditional is entered (gotoF)
def enterCond():
  res = quadruple.pilaO.pop()
  resType = helpers.getTypeV2(res)
  if resType != 'boo':
    raise Exception("ERROR! Conditional must have boolean value")
  quadruple.saveQuad('gotoF', res, -1, TBD())
  jumps.setStackPush(quadruple.quadCounter - 1)

# enterElse
# What: Saves quad and sets jump when it encounters an else value
# When is it used: Everytime an else is entered
def enterElse():
  quadruple.saveQuad('goto', -1, -1, TBD())
  falseValue = jumps.setStackPop()
  jumps.setStackPush(quadruple.quadCounter - 1)
  fill(falseValue, quadruple.quadCounter)

# exitIf
# What: Sets pending jump from conditional
# When is it used: Everytime a conditional is exited
def exitIf():
  end = jumps.setStackPop()
  fill(end, quadruple.quadCounter)

# exitWhile
# What: Saves quad and fills pending jump from while loop
# When is it used: Everytime a while loop is exited
def exitWhile():
  end = jumps.setStackPop()
  ret = jumps.setStackPop()
  quadruple.saveQuad('goto', -1, -1, ret)
  fill(end, quadruple.quadCounter)

# exitDoWhile
# What: Saves quad for exiting do while loop
# When is it used: Everytime a do while loop is exited
def exitDoWhile():
  ret = jumps.setStackPop()
  cond = quadruple.pilaO.pop()
  quadruple.saveQuad('gotoV', cond, -1, ret)

# saveForMain
# What: Sets a pending jump in quad 1, pending for main
# When is it used: At the beginning of a program
def saveForMain():
  jumps.setStackPush(quadruple.quadCounter)
  quadruple.saveQuad("goto", -1, -1, TBD())

# enterMain
# What: Generates the GOTO value in quad 1
# When is it used: When a main function is read
def enterMain():
  ret = jumps.setStackPop() 
  fill(ret, quadruple.quadCounter)
