from quad import Quad
# from symbolTable import SymbolTable
# import quadHelpers

# quadruple = Quad.instantiate()
# symbolTable = SymbolTable.instantiate()

# quadruple = Quad.instantiate()
# symbolTable = SymbolTable.instantiate()
# globalScope = SymbolTable.getGlobalScope()

# def getScopeByFuncName(quad):
#   if not quad[-1] in globalScope.keys():
#     raise Exception("Wrong mem address when finding scope")
#   return globalScope[quad[-1]]

# def assignValueToMemSpace(address, currentScope):
#   addressType = quadHelpers.getTypeV2(address) # gets if local
#   # symbolTable[currentScope].getVar

functionsReturning = {}
currentScope = None

memNumbers = {
  "globalInt": 5000,
  "globalInts": 7000,
  "globalFlt": 9000,
  "globalFlts": 11000,
  "globalCha": 13000,
  "globalChas": 15000,
  "globalBoo": 17000,
  "globalBoos": 19000,
  "globalStr": 21000,
  "globalStrs": 23000,

  "localInt": 25000,
  "localInts": 27000,
  "localFlt": 29000,
  "localFlts": 31000,
  "localCha": 33000,
  "localChas": 35000,
  "localBoo": 37000,
  "localBoos": 39000,
  "localStr": 41000,
  "localStrs": 43000,

  "constInt": 45000,
  "constFlt": 47000,
  "constCha": 49000,
  "constBoo": 51000,
  "constStr": 53000,
}

cont = 0

def getTempOffset(address):
  return address + 1000

def getConstType(address):
  return

def getClassification(address):
  if address >= 45000 and address < 55000:
    return 'const'
  elif address >= 25000 and address < 45000:
    return 'local'
  elif address >= 5000 and address < 25000:
    return 'global'
  else:
    raise Exception("ERROR! Memory out of bounds")

# def getByVirtualAddress(address, scope):
#   for key, val in scope.getScopeVariables():
#     # if 

class MemSpaceContainer:
  def __init__(self, initialAddress):
    self.__initialAddress = initialAddress
    self.__offset = 0

  def getInitialAddress(self):
    return self.__initialAddress

  def getOffset(self):
    return self.__offset
  
  def setOffset(self):
    self.__offset += 1

  def resetOffset(self):
    self.__offset = 0

  def setDimensionalOffset(self, val):
    self.__offset += val

# this is the main directory for memory addresses separated by scope
# elements contain their offset for when assigning new variables
class MemoryContainer:
  def __init__(self, name):
    self.name = name
    self.memSpace = {
      'global': {
        'int': {
          'real': MemSpaceContainer(5000),
          'temp': MemSpaceContainer(6000),
        },
        'ints': {
          'real': MemSpaceContainer(7000),
          'temp': MemSpaceContainer(8000),
        },
        'flt': {
          'real': MemSpaceContainer(9000),
          'temp': MemSpaceContainer(10000),
        },
        'flts': {
          'real': MemSpaceContainer(11000),
          'temp': MemSpaceContainer(12000),
        },
        'cha': {
          'real': MemSpaceContainer(13000),
          'temp': MemSpaceContainer(14000),
        },
        'chas': {
          'real': MemSpaceContainer(15000),
          'temp': MemSpaceContainer(16000),
        },
        'boo': {
          'real': MemSpaceContainer(17000),
          'temp': MemSpaceContainer(18000),
        }, 
        'boos': {
          'real': MemSpaceContainer(19000),
          'temp': MemSpaceContainer(20000),
        }, 
        'str': {
          'real': MemSpaceContainer(21000),
          'temp': MemSpaceContainer(22000),
        },
        'strs': {
          'real': MemSpaceContainer(23000),
          'temp': MemSpaceContainer(24000),
        },
      }, 
      'local': {
        'int': {
          'real': MemSpaceContainer(25000),
          'temp': MemSpaceContainer(26000),
        },
        'ints': {
          'real': MemSpaceContainer(27000),
          'temp': MemSpaceContainer(28000),
        },
        'flt': {
          'real': MemSpaceContainer(29000),
          'temp': MemSpaceContainer(30000),
        },
        'flts': {
          'real': MemSpaceContainer(31000),
          'temp': MemSpaceContainer(32000),
        },
        'cha': {
          'real': MemSpaceContainer(33000),
          'temp': MemSpaceContainer(34000),
        },
        'chas': {
          'real': MemSpaceContainer(35000),
          'temp': MemSpaceContainer(36000),
        },
        'boo': {
          'real': MemSpaceContainer(37000),
          'temp': MemSpaceContainer(38000),
        }, 
        'boos': {
          'real': MemSpaceContainer(39000),
          'temp': MemSpaceContainer(40000),
        },
        'str': {
          'real': MemSpaceContainer(41000),
          'temp': MemSpaceContainer(42000),
        },
        'strs': {
          'real': MemSpaceContainer(43000),
          'temp': MemSpaceContainer(44000),
        },
      },
      'constants': {
        'int': MemSpaceContainer(45000),
        'flt': MemSpaceContainer(47000),
        'cha': MemSpaceContainer(49000),
        'boo': MemSpaceContainer(51000), 
        'str': MemSpaceContainer(53000),
      }
    }
class VM:
  def __init__(self, quadList, dirFunc, dirClass):
    self.__quadList = quadList
    self.__nextPointer = 1
    self.__callStack = []
    # self.__constTable = dirFunc.getScopeConstants()
    self.__dirFunc = dirFunc
    self.__dirClass = dirClass

  def getDirFunc(self):
    return self.__dirFunc

  def getDirClass(self):
    return self.__dirClass 

  # Call Stack access
  def pushCallStack(self, functionCall):
    self.__callStack.append(functionCall)

  def popCallStack(self):
    if self.__callStack:
      return self.__callStack.pop()

  def topCallStack(self):
    if self.__callStack:
      return self.__callStack[-1]

  # Processing Operations
  # def add(self, leftDir, rightDir, resultDir):
  #   leftValue = 
  #   rightValue = 
  #   MainMemory[resultDir] = leftValue + rightValue
  # Finding value by virtual addresses from scopes
  def add(self):
    # return findValueOp1 + findValueOp1 value
    return False

  def subtract(self, leftDir, rightDir, resultDir):
    return False

  def multiply(self, leftDir, rightDir, resultDir):
    return False

  def divide(self, leftDir, rightDir, resultDir):
    return False

  def assign(self, leftDir, rightDir):
    return False
    # check if value is constant, there is no problem assigning
    # if getClassification(rightDir) == 'const':

    # check if value is variable, it might not be declared yet

    # if its a function return, we assign it to the global dictionary
    # if leftDir in self.__dirFunc:
    #   pass
    # #   pointer = self.__dirFunc[leftDir]
    # #   getByVirtualAddress(pointer.getVirtualAddress())
    # else:
      # leftOp = getByVirtualAddress(leftDir)
      # rightOp = getByVirtualAddress(rightDir)
      # leftOp.setValue(rightOp.getValue())
    # return False

  def lt(self, leftDir, rightDir, resultDir):
    return False
      
  def gt(self, leftDir, rightDir, resultDir):
    return False
      
  def le(self, leftDir, rightDir, resultDir):
    return False
      
  def ge(self, leftDir, rightDir, resultDir):
    return False
      
  def equal(self, leftDir, rightDir, resultDir):
    return False
      
  def notEqual(self, leftDir, rightDir, resultDir):
    return False

  def printLine(self, resultDir):
    print()

  def readLine(self):
    return False
      
  def goto(self, quadNumber):
    # pointing nextPointer to nextQuad
    self.__nextPointer = quadNumber
      
  def gotoF(self, tempVal, quadNumber):

    return False

  def gotoV(self):
    return False
      
  def goSub(self):
    return False

  def era(self):
    return False
  
  def param(self):
    return False

  def endFunc(self):
    return False
  
  def ver(self):
    return False
  
  def funcReturn(self):
    return False


  def end(self):
    print("---SUCCESSFUL EXECUTION---")
    
  #MAIN VM PROGRAM
  def execute(self):
    operCode = self.__quadList[self.__nextPointer].getOp()
    while (operCode < 24):
      currentQuad = self.__quadList[self.__nextPointer]
      if operCode == 1: #sumar
        self.add(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1
      
      elif operCode == 2: #restar
        self.subtract(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 3: #multiplicar
        self.multiply(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 4: #dividir
        self.divide(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 5: # assign
        self.assign(currentQuad.getLeft(), currentQuad.getRes())

      elif operCode == 6: # less than
        self.lt(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 7: # greater than
        self.gt(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 8: # less than equals
        self.le(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 9: # greater than equals
        self.ge(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 10: # equal
        self.equal(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 11: # not equal
        self.notEqual(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        self.__nextPointer += 1

      # TODO PRINT
      elif operCode == 12:
        self.printLine(currentQuad.getRes())
        self.__nextPointer += 1

      # TODO READ
      elif operCode == 13:
        self.readLine(currentQuad.getRes())
        self.__nextPointer += 1
      
      elif operCode == 14:
        # if self.__nextPointer == 1:
        self.__nextPointer = currentQuad.getRes()
        # else:

        # self.goto()
      
      elif operCode == 15:
        # self.gotoF()
        # add boolean logic
        self.__nextPointer = currentQuad.getRes()
      
      elif operCode == 16:
        # self.gotoV()
        self.__nextPointer = currentQuad.getRes()
        
      elif operCode == 17:
        # self.goSub()
        self.__nextPointer = currentQuad.getRes()

      elif operCode == 18:
        self.era()

      elif operCode == 19:
        self.param()

      elif operCode == 20:
        self.endFunc()
      
      elif operCode == 21:
        self.ver()
      
      elif operCode == 22:
        self.funcReturn()
      
      elif operCode == 23:
        # create a space in the stack with the local memory
        self.end()
      
      operCode = self.__quadList[self.__nextPointer].getOp()
    
    self.end()
     
# works like a Memory SCOPE, divided in G, L, T, C, and Objs      
class MainMemory:
  isAlive = None
  # ["global" [reales]  [temp]]
  # ["localFunc1" [varsLocalesMemoria] [tempsGenerados]]
  # [Constantes consts con direcciones de mmeoria]
  def __init__(self):
    MainMemory.isAlive = self
    self.__global = {}
    self.__local = {}
    self.__constants = {}
    self.__classes = {}
    self.__pointer = None
  
  def getGlobal(self):
    return self.__global

  def getLocal(self):
    return self.__local

  def getConstants(self):
    return self.__constants

  def getClasses(self):
    return self.__classes

  def getPointer(self):
    return self.__pointer
  
  # def setPointer(self):

  @classmethod
  def instantiate(cls):
    if MainMemory.isAlive is None:
      MainMemory()
    return MainMemory.isAlive

# def mainFunc()