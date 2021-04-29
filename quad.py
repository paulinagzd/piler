from re import split
from symbolTable import SymbolTable
from semanticCube import SemanticCube
import ast

class Quad:
  def __init__(self):
      self.pOper = []
      self.pilaO = []


  def clearQuad(self):
    self.pOper.clear()
    self.pilaO.clear()

