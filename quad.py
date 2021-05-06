from re import split
from jumps import TBD

class Quad:
  isAlive = None

  def __init__(self):
      Quad.isAlive = self
      self.pOper = []
      self.pilaO = []
      self.quads = {}
      self.quadCounter = 1

  @classmethod
  def instantiate(cls):
    if Quad.isAlive is None:
      Quad()
    return Quad.isAlive

  def saveQuad(self, operator, leftOperand, rightOperand, tvalue):
    q = QuadContainer(self.quadCounter, operator, leftOperand, rightOperand, tvalue)
    self.quads[self.quadCounter] = q
    self.quadCounter += 1

  def getWorkingStack(self):
    workingStack = []
    if '(' not in self.pOper:
      workingStack = self.pOper[0:]
      return workingStack
    elif self.pOper[-1] == '(':
      return workingStack
    else:
      for i in range(len(self.pOper)-2, -1, -1):
        index = i
        if self.pOper[i] == '(':
          break
      workingStack = self.pOper[index + 1:]
      return workingStack
  
  def reset(self):
    self.pOper = []
    self.pilaO = []
    self.quads = {}
    self.quadCounter = 1

    
  def print(self):
    for item, value in self.quads.items():
      print(item, ': ', value)
      
class QuadContainer:
  isAlive = None

  def __init__(self, ide, op, left, right, res):
    QuadContainer.isAlive = self
    self.__id = ide
    self.__op = op
    self.__left = left
    self.__right = right
    self.__res = res

  @classmethod
  def instantiate(cls):
    if QuadContainer.isAlive is None:
      QuadContainer()
    return QuadContainer.isAlive

  def getId(self):
    return self.__id
  
  def getOp(self):
      return self.__op

  def getLeft(self):
    return self.__left

  def getRight(self):
    return self.__right

  def getRes(self):
    return self.__res
  
  def setId(self, val):
    self.__id = val

  def setJump(self, val):
    if not isinstance(self.getRes(), TBD):
      raise Exception("ERROR! Quad has no pending jump")
    self.__res = val

  def __repr__(self):
    return "{%s %s %s %s %s}" % (self.getId(), self.getOp(), self.getLeft(), self.getRight(), self.getRes())
class QuadsStack:
  isAlive = None
  cont = 0

  def __init__(self):
    QuadsStack.isAlive = self
    self.__stack = []

  @classmethod
  def instantiate(cls):
    if QuadsStack.isAlive is None:
      QuadsStack()
    return QuadsStack.isAlive

  
