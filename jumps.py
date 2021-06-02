################################################
# JUMPS: class used for keeping track of the quadruple
# jumps in linear and nonlinear code events
class Jumps:
  isAlive = None

  def __init__(self):
    Jumps.isAlive = self
    self.__stack = []

  @classmethod
  def instantiate(cls):
    if Jumps.isAlive is None:
      Jumps()
    return Jumps.isAlive
  
  def getStack(self):
    return self.__stack

  def setStackPush(self, val):
    self.__stack.append(val)

  def setStackPop(self):
    return self.__stack.pop()

################################################
# TBD: class for pending jumps to be assigned an object.
# This value will change when GOTOs are fulfilled through
# helper functions
class TBD:
  pass
