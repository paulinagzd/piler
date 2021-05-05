from re import split
from symbolTable import SymbolTable
from semanticCube import SemanticCube
    
class Quad:
  isAlive = None

  def __init__(self):
      Quad.isAlive = self
      self.pOper = []
      self.pilaO = []
      self.quads = []
      self.quadCounter = 0

  @classmethod
  def instantiate(cls):
    if Quad.isAlive is None:
      Quad()
    return Quad.isAlive

  def saveQuad(self, operator, leftOperand, rightOperand, tvalue):
    self.quadCounter += 1
    q = (self.quadCounter, operator, leftOperand, rightOperand, tvalue)
    self.quads.append(q)

  def getWorkingStack(self):
    workingStack = []
    if '(' not in self.pOper:
      workingStack = self.pOper
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
      
class QuadContainer:
  isAlive = None

  def __init__(self, op, left, right, res):
    QuadContainer.isAlive = self
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
    # if not isinstance(self.__result, PendingJump):
    #   raise Exception("Trying to set a jump but this quadruple does not have a pending jump")
    self.__res = val


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

  
