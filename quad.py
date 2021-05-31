from re import split
from jumps import TBD

class Quad:
  isAlive = None
  operCodes = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '=': 5,
    '<': 6,
    '>': 7,
    '<=': 8,
    '>=': 9,
    '==': 10,
    '!=': 11,
    '&&': 12,
    '||': 13,
    'print': 14,
    'read': 15,
    'goto': 16,
    'gotoF': 17,
    'gotoV': 18,
    'gosub': 19,
    'era': 20,
    'param': 21,
    'endfunc': 22,
    'verify' : 23,
    'return' : 24,
    'end': 25,
    '+a': 26,
    '*a': 27,
  }

  def __init__(self):
      Quad.isAlive = self
      self.pOper = []
      self.pilaO = []
      self.pilaDim = []
      self.pilaArr = []
      self.quads = {}
      self.quadCounter = 1

  @classmethod
  def instantiate(cls):
    if Quad.isAlive is None:
      Quad()
    return Quad.isAlive

  def saveQuad(self, operator, leftOperand, rightOperand, tvalue):
    codeNumber = self.operCodes[operator]
    q = QuadContainer(codeNumber, leftOperand, rightOperand, tvalue) # left and right operand contain ADDRESSES
    # q = QuadContainer(self.quadCounter, operator, leftOperand, rightOperand, tvalue) # left and right operand contain ADDRESSES
    self.quads[self.quadCounter] = q
    self.quadCounter += 1
    print(q)

  def getWorkingStack(self):
    workingStack = []
    if '(' not in self.pOper:
      workingStack = self.pOper[0:]
      return workingStack
    elif self.pOper[-1] == '(' or self.pOper[-1] == '{':
      return workingStack
    else:
      for i in range(len(self.pOper)-2, -1, -1):
        index = i
        if self.pOper[i] == '(' or self.pOper[i] == '{':
          break
      workingStack = self.pOper[index + 1:]
      return workingStack
  
  def reset(self):
    self.pOper = []
    self.pilaO = []
    self.pilaDim = []
    self.pilaArr = []
    self.quads = {}
    self.quadCounter = 1

    
  def print(self):
    for item, value in self.quads.items():
      print(item, ': ', value)
      
class QuadContainer:
  isAlive = None

  def __init__(self, op, left, right, res):
    QuadContainer.isAlive = self
    # self.__id = ide
    self.__op = op
    self.__left = left
    self.__right = right
    self.__res = res

  @classmethod
  def instantiate(cls):
    if QuadContainer.isAlive is None:
      QuadContainer()
    return QuadContainer.isAlive

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
    return "{%s %s %s %s}" % (self.getOp(), self.getLeft(), self.getRight(), self.getRes())

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

  
