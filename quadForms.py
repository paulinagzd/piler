from symbolTable import SymbolTable
from semanticCube import SemanticCube

s = SymbolTable.getInstance() # singletonInstance


#aritmeticos
def quad(pOper, pilaO, latestId):
  #
  # t1
  i = 0
  temp = [] # + 2 2
  table = {} # 0: + 2 2 t1
  while pilaO:
    val = pilaO.pop(0)
    temp.append(val)
    if len(temp) == 2:
      # haz operacion
      currOp = pilaO.pop(0)
      temp.insert(0, currOp)
      table[i] = temp
      pilaO.insert(0, table[i].values)

  if not pOper:
    varType = SemanticCube.returningType(temp)
    varValue = 4

