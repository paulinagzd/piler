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

  def setDimensionalOffset(self, val):
    self.__offset += val

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
  def __init__(self, quadList):
    self.__quadList = quadList
    self.__nextPointer = 1

  # Processing Operations
  def add(self):
    return False

  def subtract(self):
    return False

  def multiply(self):
    return False

  def divide(self):
    return False  

  def assign(self):
    return False

  def lt(self):
    return False
      
  def gt(self):
    return False
      
  def le(self):
    return False
      
  def ge(self):
    return False
      
  def equal(self):
    return False
      
  def notEqual(self):
    return False

  def printLine(self):
    return False

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
    
  #MAIN VM PROGRAM
  def driverProgram(self):
    operCode = quadList[nextPointer][0]
    while (operCode != 21):
      if operCode == 1: #sumar
        self.add()

      elif operCode == 2:
        self.subtract()

      elif operCode == 3:
        self.multiply()

      elif operCode == 4:
        self.divide()

      elif operCode == 5:
        self.assign()

      elif operCode == 6:
        self.lt()

      elif operCode == 7:
        self.gt()

      elif operCode == 8:
        self.le()

      elif operCode == 9:
        self.ge()

      elif operCode == 10:
        self.equal()

      elif operCode == 11:
        self.notEqual()

      elif operCode == 12:
        self.printLine()

      elif operCode == 13:
        self.readLine()
      
      elif operCode == 14:
        self.goto()
      
      elif operCode == 15:
        self.gotoF()
      
      elif operCode == 16:
        self.gotoV()
        
      elif operCode == 17:
        self.goSub()

      elif operCode == 18:
        self.era()

      elif operCode == 19:
        self.param()

      elif operCode == 20:
        self.endFunc()
      
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
