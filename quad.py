from re import split
from symbolTable import SymbolTable
from semanticCube import SemanticCube

class Quad:
  def __init__(self):
      self.pOper = []
      self.pilaO = []

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
      