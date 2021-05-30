from ast import literal_eval
from quad import Quad

functionsReturning = {}
currentScope = None
arrParam = []
paramCont = 0
returnVal = 0

def getTypeConstant(operand):
  if operand == 'True' or operand == 'False':
    return 'boo'
  elif isinstance(operand,float):
    return 'flt'
  elif isinstance(operand,int):
    return 'int'
  elif isinstance(operand, str):
    if len(operand) == 1:
      return 'cha'
    else:
      return 'str'

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
scopePointer = None

def getTempOffset(address):
  return address + 1000

def getConstType(address):
  return

def verifySize(funcSize, mem):
  for i, j in funcSize["local"].items():
    if j + mem.localMem.variables[i] <= 1000:
      mem.localMem.variables[i] += j
      # print(MainMemory.instantiate().localMem.variables[i])
    else:
      raise Exception("ERROR! Stack overflow")

  for i, j in funcSize["temps"].items():
    if j + mem.localMem.temps[i] <= 1000:
      mem.localMem.temps[i] += j
      # print( MainMemory.instantiate().localMem.temps[i])
    else:
      raise Exception("ERROR! Stack overflow")

def generateERA(funcName, scope):
  dirFunc = VM.get().getDirClass() if scope == 'class' else VM.get().getDirFunc()
  mem = MainMemory.instantiate()
  global scopePointer
  if scope == 'class':
    for i in dirFunc:
      if funcName in i['global']['funcs']:
        funcSize = i['global']['funcs'][funcName]["size"]
        verifySize(funcSize, mem)
        scopePointer = {funcName: i['global']['funcs'][funcName]}
  else:
    funcSize = dirFunc['global']['funcs'][funcName]["size"]
    verifySize(funcSize, mem)
    scopePointer = {funcName: dirFunc['global']['funcs'][funcName]}

  return True

# def freeMemory(funcName, scope):
#   dirFunc = VM.get().getDirClass() if scope == 'class' else VM.get().getDirFunc()
#   mem = MainMemory.instantiate()
#   global scopePointer
#   if scope == 'class':
#     for i in dirFunc:
#       if funcName in i['global']['funcs']:
#         funcSize = i['global']['funcs'][funcName]["size"]
#         verifySize(funcSize, mem)
#         scopePointer = {funcName: i['global']['funcs'][funcName]}
#   else:
#     funcSize = dirFunc['global']['funcs'][funcName]["size"]
#     verifySize(funcSize, mem)
#     scopePointer = {funcName: dirFunc['global']['funcs'][funcName]}

def getClassification(address):
  if address >= 45000 and address < 55000:
    return 'const'
  elif address >= 25000 and address < 45000:
    return 'local'
  elif address >= 5000 and address < 25000:
    return 'global'
  else:
    raise Exception("ERROR! Memory out of bounds")

def point(address):
  mem = MainMemory.instantiate()
  if getClassification(address) == 'const':
    return mem.getConstants()
    # mem.setPointer(mem.getConstants())
  elif getClassification(address) == 'local':
    # print("POINTING TO LOCAL")
    # global goHere
    # goHere = mem.getLocal()[list(VM.get().topCallStack())[0]]
    curr = mem.getLocal()
    # print("GET LOCAL", curr)
    mem.setPointer(curr[list(VM.get().topCallStack())[0]])
    # mem.setPointer(mem.getPointer().)
  else:
    mem.setPointer(mem.getGlobal())

  return mem.getPointer()

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
  isAlive = None
  def __init__(self, quadList, dirFunc, dirClass):
    VM.isAlive = self
    self.__quadList = quadList
    self.__nextPointer = 1
    self.__callStack = []
    # self.__constTable = dirFunc.getScopeConstants()
    self.__dirFunc = dirFunc
    self.__dirClass = dirClass

    mem = MainMemory.instantiate()
    mem.setGlobal(dirFunc)
    mem.setPointer(mem.getGlobal())
    mem.setConstants(dirFunc)

  @classmethod
  def instantiate(cls, param1, param2, param3):
    if VM.isAlive is None:
      VM(param1, param2, param3)
    return VM.isAlive

  @classmethod
  def get(cls):
    if VM.isAlive is not None:
      return VM.isAlive


  def getDirFunc(self):
    return self.__dirFunc

  def getDirClass(self):
    return self.__dirClass 

  # Call Stack access
  def pushCallStack(self, functionCall, goHere):
    self.__callStack.append(functionCall)
    mem = MainMemory.instantiate()
    mem.setLocal(functionCall, goHere)
    # print("CALLSTACK")
    # print(self.__callStack)

  def popCallStack(self):
    if self.__callStack:
      #liberar memoria
      #1. volver a poner como None las variables y los temporales utilizados
      #2. bajar el counter de direcciones memorias usadas
      mem = MainMemory.instantiate()
      curr = mem.localMem.variables
      for i, j in curr.items():
        curr[i] -= j      
    self.__callStack.pop()

  def topCallStack(self):
    if self.__callStack:
      return self.__callStack[-1]

  # Processing Operations
  # def add(self, leftDir, rightDir, resultDir):
  #   leftValue = 
  #   rightValue = 
  #   MainMemory[resultDir] = leftValue + rightValue
  # Finding value by virtual addresses from scopes

  def getPointerType(self, address):
    return point(address)

  def assignValueToDir(self, value, pointer, key):
    pointer[key] = value
    # print("ASSIGN VALUE TO DIR", pointer[key], value)

  def add(self, leftVal, rightVal):
    return leftVal + rightVal

  def subtract(self, leftVal, rightVal):
    return leftVal - rightVal

  def multiply(self, leftVal, rightVal):
    return leftVal * rightVal

  def divide(self, leftVal, rightVal):
    return leftVal / rightVal

  def assign(self, assignWhat, assignWhatDir, assignTo, assignToDir):
    self.assignValueToDir(assignWhat[assignWhatDir], assignTo, assignToDir)

  def lt(self, leftVal, rightVal):
    return leftVal < rightVal
      
  def gt(self, leftVal, rightVal):
    return leftVal > rightVal
      
  def lte(self, leftVal, rightVal):
    return leftVal <= rightVal
      
  def gte(self, leftVal, rightVal):
    # print()
    return leftVal >= rightVal
      
  def equal(self, leftVal, rightVal):
    return leftVal == rightVal
      
  def notEqual(self, leftVal, rightVal):
    return leftVal != rightVal

  def printLine(self, val):
    print(val)

  def readLine(self, type):
    inValue = input('> ')
    inValueType = getTypeConstant(literal_eval(inValue))
    if type == inValueType:
      return inValue
    else:
      raise Exception(ValueError, SyntaxError)
    # print("INVVALUE", inValue)
    # return inValue
      
  def goto(self, quadNumber):
    # pointing nextPointer to nextQuad
    self.__nextPointer = quadNumber
      
  def gotoF(self, tempVal, quadNumber):

    return False

  def gotoV(self):
    return False
      
  def goSub(self):
    return False

  def era(self, funcName, scope):
    if generateERA(funcName, scope) == True:
      self.__nextPointer += 1
    # else:
    #   raise Exception("ERROR! Stack overflow")

    # return False
  def param(self, paramPoint, paramDir):
    global paramCont
    global arrParam
    arrParam.append(paramPoint[paramDir])
    # print("LEN ARR PARAM", len(arrParam))
    # paramCont += 1
    # return

  def endFunc(self):
    return False
  
  def ver(self):
    return False
  
  def funcReturn(self, retPointer, retAddress):
    # access value I want to send
    valueToSend = retPointer[retAddress]
    return valueToSend
  
  def binaryOps(self, left, right, result):
    res = []
    res.append(self.getPointerType(left))
    res.append(self.getPointerType(right))
    res.append(self.getPointerType(result))
    return res

  def end(self):
    print("---SUCCESSFUL EXECUTION---")
    
  #MAIN VM PROGRAM
  def execute(self):
    global arrParam
    global paramCont
    global returnVal
    operCode = self.__quadList[self.__nextPointer].getOp()
    while (operCode < 24):
      # print("OPERCODE", operCode)
      currentQuad = self.__quadList[self.__nextPointer]
      if operCode == 1: #sumar
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        # print(pointers[0], pointers[1], pointers[2])
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Adding null values")
        res = self.add(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1
      
      elif operCode == 2: #restar
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Subtracting null values")
        res = self.subtract(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 3: #multiplicar
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0][currentQuad.getLeft()] == None or pointers[1][currentQuad.getRight()] == None:
          raise Exception("ERROR! Multiplying null values")
          
        res = self.multiply(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 4: #dividir
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Dividing null values")
        res = self.divide(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 5: # assign
        if isinstance(currentQuad.getLeft(), str):
          assignTo = self.getPointerType(currentQuad.getRes())
          assignTo[currentQuad.getRes] = returnVal
          returnVal = None
        else:
          assignWhat = self.getPointerType(currentQuad.getLeft())
          assignTo = self.getPointerType(currentQuad.getRes())
          # print(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
          self.assign(assignWhat, currentQuad.getLeft(), assignTo, currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 6: # less than
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.lt(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 7: # greater than
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.gt(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 8: # less than equals
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.lte(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 9: # greater than equals
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.gte(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 10: # equal
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.equal(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      elif operCode == 11: # not equal
        pointers = self.binaryOps(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        if pointers[0] == None or pointers[1] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.notEqual(pointers[0][currentQuad.getLeft()], pointers[1][currentQuad.getRight()])

        self.assignValueToDir(res, pointers[2], currentQuad.getRes())
        self.__nextPointer += 1

      # TODO PRINT
      elif operCode == 12:
        self.printLine(self.getPointerType(currentQuad.getRes())[currentQuad.getRes()])
        self.__nextPointer += 1

      # TODO READ
      elif operCode == 13:
        # print("READ TO ASSIGN TO THIS ADDRESS", currentQuad.getRes())

        toReadPointer = self.getPointerType(currentQuad.getRes())

        res = self.readLine(getTypeConstant(currentQuad.getRes()))
        self.assignValueToDir(int(res), toReadPointer, currentQuad.getRes())

        self.__nextPointer += 1
      
      elif operCode == 14: # goto
        # if self.__nextPointer == 1:
        self.__nextPointer = currentQuad.getRes()
        # else:

        # self.goto()
      
      elif operCode == 15: # gotoF
        # self.gotoF()
        # add boolean logic
        self.__nextPointer = currentQuad.getRes()
      
      elif operCode == 16: # gotoV
        # self.gotoV()
        self.__nextPointer = currentQuad.getRes()
        
      elif operCode == 17: # goSub
        # self.goSub()
        # print("LLEGO GOSUB")
        global scopePointer
        VM.get().pushCallStack(scopePointer, self.__nextPointer + 1)
        arrParam = []
        paramCont = 0
        calledFunction = VM.get().topCallStack()
        self.__nextPointer = calledFunction[list(calledFunction)[0]]["start"]

      elif operCode == 18: # era
        self.era(currentQuad.getLeft(), currentQuad.getRight())
        # self.__nextPointer += 1

      elif operCode == 19: # param
        paramDir = currentQuad.getLeft()
        paramPoint = self.getPointerType(paramDir)
        self.param(paramPoint, paramDir)
        self.__nextPointer += 1

      elif operCode == 20: # endfunc
        self.endFunc()
        self.__nextPointer += 1

      elif operCode == 21: # verify
        self.ver()
        self.__nextPointer += 1

      elif operCode == 22: # return
        print("RETURN")
        retAddress = currentQuad.getRes()
        retPointer = self.getPointerType(retAddress)
        returnVal = self.funcReturn(retPointer, retAddress)
        # regresa a migajita de pan
        # if getClassification(retPointer[retAddress]) == 'const':

        print("GOHERE", retPointer, retAddress)
        goHere = MainMemory.instantiate().getPointer()["goHere"]
        # pop from Call Stack
        VM.get().popCallStack()
        self.__nextPointer = goHere

      elif operCode == 23: # end
        # create a space in the stack with the local memory
        self.end()
        print("TERMINO CON EXITO")
        return False
        self.__nextPointer += 1

      print(self.__nextPointer)
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
    self.globalMem = CallStackMemory()
    self.__local = {}
    self.localMem = CallStackMemory()
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
  
  def setPointer(self, val):
    self.__pointer = val

  def setGlobal(self, dirFunc):
    globalVars = dirFunc["global"]["vars"]
    for i, j in globalVars.items():
      self.__global[j.getVirtualAddress()] = None
      # print(i, j)
    
    globalTemps = dirFunc["global"]["temps"]
    for i, j in globalTemps.items():
      self.__global[j.getVirtualAddress()] = None

    # print("ESTA LINEA")
    # for i in self.__global:
    #   print(i)
  def setLocal(self, functionCall, goHere):
    # sends a dictionary with function name: attributes
    # print("SET LOCAL")
    funcName = list(functionCall)[0]
    # migajita de pan
    self.__local[funcName] = {}
    pointerVars = functionCall[funcName]['vars']
    pointerTemps = functionCall[funcName]['temps']
    for i, j in pointerVars.items():
      if j.getIsParam():
        global arrParam
        global paramCont
        # print("PARAM ARR", arrParam)
        # print("PARAM CONT", paramCont)
        # assign temp value from arrParam
        self.__local[funcName][j.getVirtualAddress()] = arrParam[paramCont]
        paramCont += 1
      else:
        self.__local[funcName][j.getVirtualAddress()] = None
    for i, j in pointerTemps.items():
      self.__local[funcName][j.getVirtualAddress()] = None
    self.__local[funcName]["goHere"] = goHere
    # print(self.__local[funcName])

  def setConstants(self, dirFunc):
    consts = dirFunc["global"]["consts"]
    for i, j in consts.items():
      for k, l in j.items():
        self.__constants[l] = k
    
    # print("ESTA LINEA")
    # for i in self.__constants:
    #   print(i)
  
  # def setPointer(self):

  @classmethod
  def instantiate(cls):
    if MainMemory.isAlive is None:
      MainMemory()
    return MainMemory.isAlive

# def mainFunc()

class CallStackMemory:
  def __init__(self):
    self.variables = {
      'int': 0,
      'flt': 0,
      'boo': 0,
      'cha': 0,
      'str': 0,
      'ints': 0,
      'flts': 0,
      'boos': 0,
      'chas': 0,
      'strs': 0
    }
    self.temps = {
      'int': 0,
      'flt': 0,
      'boo': 0,
      'cha': 0,
      'str': 0,
      'ints': 0,
      'flts': 0,
      'boos': 0,
      'chas': 0,
      'strs': 0
    }
  
  # añadir objetos a la call stack memory
  # apuntar a funcion (en symbol table)
