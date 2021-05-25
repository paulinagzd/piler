from quad import Quad

quadruple = Quad.instantiate()

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

# this is the main directory for memory addresses separated by scope
# elements contain their offset for when assigning new variables
memSpace = {
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
  def __init__(self, quadList, ):
    self.__quadList = quadList
    self.__nextPointer = 1
    self.__callStack = []
  
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
  def add(self, leftDir, rightDir, resultDir):
    leftValue = 
    rightValue = 
    MainMemory[resultDir] = leftValue + rightValue
    return False

  def subtract(self, leftDir, rightDir, resultDir):
    return False

  def multiply(self, leftDir, rightDir, resultDir):
    return False

  def divide(self, leftDir, rightDir, resultDir):
    return False

  def assign(self):
    return False

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
      
  def goto(self):
    return False
      
  def gotoF(self):
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
    operCode = self.__quadList[self.__nextPointer][0]
    while (operCode < 23):
      currentQuad = self.__quadList[self.__nextPointer]
      if operCode == 1: #sumar
        self.add(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1
      
      elif operCode == 2: #restar
        self.subtract(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 3: #multiplicar
        self.multiply(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 4: #dividir
        self.divide(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 5: 
        self.assign()

      elif operCode == 6:
        self.lt(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 7:
        self.gt(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 8:
        self.le(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 9:
        self.ge(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 10:
        self.equal(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 11:
        self.notEqual(currentQuad[1], currentQuad[2], currentQuad[3])
        self.__nextPointer += 1

      elif operCode == 12:
        self.printLine()
        self.__nextPointer += 1

      elif operCode == 13:
        self.readLine()
        self.__nextPointer += 1
      
      elif operCode == 14:
        self.goto()
        self.__nextPointer = currentQuad[3]
      
      elif operCode == 15:
        self.gotoF()
        # add boolean logic
        self.__nextPointer = currentQuad[3]
      
      elif operCode == 16:
        self.gotoV()
        self.__nextPointer = currentQuad[3]
        
      elif operCode == 17:
        self.goSub()
        self.__nextPointer = currentQuad[3]

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
      
      operCode = self.__quadList[self.__nextPointer][0]
    
    self.end()
     
# works like a Memory SCOPE, divided in G, L, T, C, and Objs      
class MemoryContainer:
  isAlive = None

  def __init__(self):
    MemoryContainer.isAlive = self

  @classmethod
  def instantiate(cls):
    if MemoryContainer.isAlive is None:
      MemoryContainer()
    return MemoryContainer.isAlive

class MainMemory:
  isAlive = None

  def __init__(self):
    MainMemory.isAlive = self
    self.__global = {}
    self.__local = {}
    self.__constants = {}
    self.__classes = {}
  
  def getGlobal(self):
    return self.__global

  def getLocal(self):
    return self.__local

  def getConstants(self):
    return self.__constants

  def getClasses(self):
    return self.__classes

  @classmethod
  def instantiate(cls):
    if MainMemory.isAlive is None:
      MainMemory()
    return MainMemory.isAlive
