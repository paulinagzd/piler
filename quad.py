from re import split
from jumps import TBD

################################################
# QUAD: class that keeps track of all stacks used to
# create quadruples, as well as the corresponding
# operation codes. 
class Quad:
  isAlive = None

  # operation codes key and value pairs to store when saving quad
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
      self.pOper = [] # for operators
      self.pilaO = [] # for operands
      self.pilaDim = [] # for dimensions
      self.pilaArr = [] # for arrays
      self.quads = {} # our dictionary with index value pairs
      self.quadCounter = 1 # keeping an index

  @classmethod
  def instantiate(cls):
    if Quad.isAlive is None:
      Quad()
    return Quad.isAlive

  # saveQuad
  # What: stores the quadruple on the quads dictionary
  # Parameters: the operator and operands, as well as the res or temp value
  # When is it used: When any type of quadruple has to be stored for future execution
  def saveQuad(self, operator, leftOperand, rightOperand, tvalue):
    codeNumber = self.operCodes[operator]
    q = QuadContainer(codeNumber, leftOperand, rightOperand, tvalue) # left and right operand contain ADDRESSES
    self.quads[self.quadCounter] = q
    self.quadCounter += 1

  # getWorkingStack
  # What: returns stack that's being operated on in expressions
  # Parameters: none (self from class)
  # When is it used: When solving expressions, returning if it's nested or not
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
  
  # for starting over with new programs
  def reset(self):
    self.pOper = []
    self.pilaO = []
    self.pilaDim = []
    self.pilaArr = []
    self.quads = {}
    self.quadCounter = 1

  # Method used to print for debugging purposes
  def print(self):
    for item, value in self.quads.items():
      print(item, ': ', value)
      
################################################
# QUAD CONTAINER: this contains an object with
# a quadruple's four corresponding operands. It's
# instantiated from QUAD class.
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
    
  # GETTERS: used to access each element in this class
  # for operator (see operCodes in QUAD)
  def getOp(self):
      return self.__op

  # left operand
  def getLeft(self):
    return self.__left

  # right operand
  def getRight(self):
    return self.__right

  # res operand
  def getRes(self):
    return self.__res

  # used to set pending jumps in GOTO type of Quads
  def setJump(self, val):
    if not isinstance(self.getRes(), TBD):
      raise Exception("ERROR! Quad has no pending jump")
    self.__res = val
  
  # Method used to print for debugging purposes
  def __repr__(self):
    return "{%s %s %s %s}" % (self.getOp(), self.getLeft(), self.getRight(), self.getRes())
