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

class TBD:
  pass
