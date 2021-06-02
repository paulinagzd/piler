from ast import literal_eval
from quad import Quad
import helpers

functionsReturning = {}
currentScope = None
arrParam = []
localStack = []
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

def verifySize(funcSize, mem):
  for i, j in funcSize["local"].items():
    if j + mem.localMem.variables[i] <= 1000:
      mem.localMem.variables[i] += j
    else:
      raise Exception("ERROR! Too many variables!")

  for i, j in funcSize["temps"].items():
    if j + mem.localMem.temps[i] <= 1000:
      mem.localMem.temps[i] += j
    else:
      raise Exception("ERROR! Too many variables!")

def generateERA(funcName, className, scope):
  dirFunc = VM.get().getDirClass() if scope == 'class' else VM.get().getDirFunc()
  mem = MainMemory.instantiate()
  global scopePointer
  if scope == 'class':
    for j in dirFunc:
      if list(j)[0] == className:
        if funcName in j[className]['global']['funcs']:
          funcSize = j[className]['global']['funcs'][funcName]["size"]
          verifySize(funcSize, mem)
          scopePointer = {funcName: j[className]['global']['funcs'][funcName]}
  else:
    funcSize = dirFunc['global']['funcs'][funcName]["size"]
    verifySize(funcSize, mem)
    scopePointer = {funcName: dirFunc['global']['funcs'][funcName]}
  return True

def getClassification(address):
  # print("ADDRESS", address)
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
  elif getClassification(address) == 'local':
    if VM.get().topCallStack() != None:
      curr = mem.getLocalTop()
      mem.setPointer(curr)
    else:
      mem.setPointer(mem.getGlobal())
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

  def reset(self):
    VM.isAlive = None

  def getDirFunc(self):
    return self.__dirFunc

  def getDirClass(self):
    return self.__dirClass 

  def getNextPointer(self):
    return self.__nextPointer 

  # Call Stack access
  def pushCallStack(self, functionPointer, goHere):
    mem = MainMemory.instantiate()
    mem.setLocal(functionPointer, goHere)

    funcName = list(functionPointer)[0]
    functionPointer[funcName]["goHere"] = goHere
    self.__callStack.append(functionPointer)

  def popCallStack(self):
    if self.__callStack:
      #liberar memoria
      #1. volver a poner como None las variables y los temporales utilizados
      #2. bajar el counter de direcciones memorias usadas
      mem = MainMemory.instantiate()
      curr = mem.localMem.variables
      for i, j in curr.items():
        curr[i] -= j      
    return self.__callStack.pop()

  def getCallStack(self):
    return self.__callStack

  def topCallStack(self):
    if self.__callStack:
      return self.__callStack[-1]

  def getPointerType(self, address):
    return point(self.returnIsArray(address))

  def assignValueToDir(self, value, pointer, key):
    pointer[key] = value

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
    return leftVal >= rightVal
      
  def equal(self, leftVal, rightVal):
    return leftVal == rightVal
      
  def notEqual(self, leftVal, rightVal):
    return leftVal != rightVal

  def andFunc(self, leftVal, rightVal):
    return leftVal and rightVal
      
  def orFunc(self, leftVal, rightVal):
    return leftVal or rightVal

  def printLine(self, val):
    #remove quotations
    if isinstance(val, str):
      val = val.strip('"')
    print(val)

  def readLine(self, type):
    inValue = input('> ')
    inValueType = getTypeConstant(literal_eval(inValue))
    if type == inValueType:
      return inValue
    else:
      raise Exception("ERROR! Incorrect data type as input (should be", type, "received ", inValueType)
      
  def goto(self, quadNumber):
    # pointing nextPointer to nextQuad
    self.__nextPointer = quadNumber
      
  def gotoF(self, tempVal, quadNumber):

    return False

  def gotoV(self):
    return False
      
  def goSub(self):
    return False

  def era(self, funcName, scope, className):
    if generateERA(funcName, className, scope) == True:
      self.__nextPointer += 1

  def param(self, paramPoint, paramDir):
    global paramCont
    global arrParam
    arrParam.append(paramPoint[paramDir])

  # def endFunc(self):
  #   return False
  
  def ver(self, verVal, upperLim):
    if verVal < 0 or verVal > upperLim - 1:
      raise Exception("ERROR! Dimensions out of index range")
  
  def funcReturn(self, retPointer, retAddress):
    # access value I want to send
    valueToSend = retPointer[retAddress]
    return valueToSend
  
  def returnIsArray(self, address):
    if isinstance(address, list):
      address = address[0]
      # it references the content in the address
      addressScope = point(address)
      address = addressScope[address]

    return address

  def binaryOps(self, left, right, result):
    res = []
    res.append(left)
    res.append(right)
    res.append(result)
    return res

  def end(self):
    print("---SUCCESSFUL EXECUTION---")
    
  #MAIN VM PROGRAM
  def execute(self):
    global arrParam
    global paramCont
    global returnVal
    operCode = self.__quadList[self.__nextPointer].getOp()
    while (operCode < 28):
      currentQuad = self.__quadList[self.__nextPointer]
      if operCode == 1: #sumar
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Adding null values")
        res = self.add(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1
      
      elif operCode == 2: #restar
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))        
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Subtracting null values")
        res = self.subtract(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 3: # multiplicar
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))

        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Multiplying null values")
          
        res = self.multiply(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 4: #dividir
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Dividing null values")
        res = self.divide(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 5: # assign
        pointerValLeft = self.returnIsArray(currentQuad.getLeft())
        pointerValRes = self.returnIsArray(currentQuad.getRes())
        pointerLeft = self.getPointerType(currentQuad.getLeft())
        pointerRes = self.getPointerType(currentQuad.getRes())
        assignTo = pointerRes
        if isinstance(currentQuad.getLeft(), str):
          assignTo[pointerValRes] = returnVal
          returnVal = None
        else:
          assignWhat = pointerLeft
          self.assign(assignWhat, pointerValLeft, assignTo, pointerValRes)
        self.__nextPointer += 1

      elif operCode == 6: # less than
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))        
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.lt(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 7: # greater than
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.gt(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 8: # less than equals
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.lte(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 9: # greater than equals
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.gte(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 10: # equal
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.equal(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 11: # not equal
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.notEqual(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 12: # and
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.andFunc(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      elif operCode == 13: # or
        pointersVal = self.binaryOps(self.returnIsArray(currentQuad.getLeft()), self.returnIsArray(currentQuad.getRight()), self.returnIsArray(currentQuad.getRes()))
        pointers = self.binaryOps(self.getPointerType(pointersVal[0]), self.getPointerType(pointersVal[1]), self.getPointerType(pointersVal[2]))
        if pointers[0][pointersVal[0]] == None or pointers[1][pointersVal[1]] == None:
          raise Exception("ERROR! Comparing null values")
        res = self.orFunc(pointers[0][pointersVal[0]], pointers[1][pointersVal[1]])

        self.assignValueToDir(res, pointers[2], pointersVal[2])
        self.__nextPointer += 1

      # TODO PRINT
      elif operCode == 14:
        pointerVal = self.returnIsArray(currentQuad.getRes())
        self.printLine(self.getPointerType(pointerVal)[pointerVal])
        self.__nextPointer += 1

      # TODO READ
      elif operCode == 15:
        pointerVal = self.returnIsArray(currentQuad.getRes())
        toReadPointer = self.getPointerType(pointerVal)

        res = self.readLine(helpers.getTypeV2(pointerVal))
        self.assignValueToDir(int(res), toReadPointer, currentQuad.getRes())

        self.__nextPointer += 1
      
      elif operCode == 16: # goto
        self.__nextPointer = currentQuad.getRes()
      
      elif operCode == 17: # gotoF
        tempAddress = currentQuad.getLeft()
        tempType = self.getPointerType(tempAddress)
        if tempType[tempAddress]:
          self.__nextPointer += 1
        else:
          self.__nextPointer = currentQuad.getRes()
      
      elif operCode == 18: # gotoV
        tempAddress = currentQuad.getLeft()
        tempType = self.getPointerType(tempAddress)
        if not tempType[tempAddress]:
          self.__nextPointer += 1
        else:
          self.__nextPointer = currentQuad.getRes()
        
      elif operCode == 19: # goSub
        global scopePointer
        funcName = list(scopePointer)[0]
        scopePointer[funcName]["arrParam"] = arrParam
        arrParam = []
        VM.get().pushCallStack(scopePointer, self.__nextPointer + 1)
        calledFunction = VM.get().topCallStack()
        self.__nextPointer = calledFunction[funcName]["start"]

      elif operCode == 20: # era
        arrParam = []
        if currentQuad.getRes() != -1:
          self.era(currentQuad.getLeft(), currentQuad.getRight(), currentQuad.getRes())
        else:
          self.era(currentQuad.getLeft(), currentQuad.getRight(), None)


      elif operCode == 21: # param
        paramDir = currentQuad.getLeft()
        paramPoint = self.getPointerType(paramDir)
        self.param(paramPoint, paramDir)
        self.__nextPointer += 1

      elif operCode == 22: # endfunc
        # regresa a migajita de pan
        mem = MainMemory.instantiate()
        funcName = list(self.topCallStack())[0]
        goHere = mem.getLocalTop()["goHere"]
        endingFunc = self.popCallStack()
        endingLocal = mem.popLocalTop()
        self.__nextPointer = goHere
        currentQuad = self.__quadList[self.__nextPointer]
        # it returns to main (or global)

      elif operCode == 23: # verify
        verDir = currentQuad.getLeft()
        verVal = self.getPointerType(verDir)
        valToSend = verVal[verDir]
        upperLim = currentQuad.getRes()
        self.ver(valToSend, upperLim)
        self.__nextPointer += 1

      elif operCode == 24: # return
        retAddress = currentQuad.getRes()
        retPointer = self.getPointerType(retAddress)
        returnVal = self.funcReturn(retPointer, retAddress)

        # regresa a migajita de pan
        mem = MainMemory.instantiate()
        funcName = list(self.topCallStack())[0]
        goHere = mem.getLocalTop()["goHere"]
        endingFunc = self.popCallStack()
        endingLocal = mem.popLocalTop()
        self.__nextPointer = goHere
        currentQuad = self.__quadList[self.__nextPointer]
        if not self.__callStack: # return to sleeping function
          # it returns to main (or global)
          globalDir = currentQuad.getRes()
          if getClassification(globalDir) == 'global':
            globalDirVal = mem.getGlobal()
          elif getClassification(globalDir) == 'local':
            globalDirVal = mem.getLocalTop()
          else:
            globalDirVal = mem.getConstants()
          self.assignValueToDir(returnVal, globalDirVal, globalDir)
          self.__nextPointer += 1
        else:
          currLocal = mem.getLocalTop()
          newDir = currentQuad.getRes()
          newVal = self.getPointerType(newDir)
          self.assignValueToDir(returnVal, newVal, newDir)
          self.__nextPointer += 1

      elif operCode == 25: # end
        # create a space in the stack with the local memory
        self.end()
        print("TERMINO CON EXITO")
        return True
        # self.__nextPointer += 1

      elif operCode == 26: # add from arrays
        # comes from array
        leftDir = currentQuad.getLeft()
        leftVal = self.getPointerType(leftDir)
        resDir = currentQuad.getRes()
        resVal = self.getPointerType(resDir)
        res = self.add(leftVal[leftDir], currentQuad.getRight())
        self.assignValueToDir(res, resVal, resDir)
        self.__nextPointer += 1

      elif operCode == 27: # add from arrays
        # comes from array
        leftDir = currentQuad.getLeft()
        leftVal = self.getPointerType(leftDir)
        resDir = currentQuad.getRes()
        resVal = self.getPointerType(resDir)
        res = self.multiply(leftVal[leftDir], currentQuad.getRight())
        self.assignValueToDir(res, resVal, resDir)
        self.__nextPointer += 1


      operCode = self.__quadList[self.__nextPointer].getOp()
    
    # self.end()
     
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
    self.__localArr = []
    self.localMem = CallStackMemory()
    self.__constants = {}
    self.__classes = {}
    self.__pointer = None
  
  def getGlobal(self):
    return self.__global

  def getLocal(self):
    return self.__local

  def getLocalArr(self):
    return self.__localArr

  def getLocalTop(self):
    return self.__localArr[-1]

  def popLocalTop(self):
    return self.__localArr.pop()

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
    if len(globalVars) > 1000:
      raise Exception("ERROR! Too many variables!")
    for i, j in globalVars.items():
      self.__global[j.getVirtualAddress()] = j.getValue()
      
    globalTemps = dirFunc["global"]["temps"]
    for i, j in globalTemps.items():
      self.__global[j.getVirtualAddress()] = None
    if len(globalTemps) > 1000:
      raise Exception("ERROR! Too many variables!")   

  def setLocal(self, functionPointer, goHere):
    # sends a dictionary with function name: attributes
    funcName = list(functionPointer)[0]
    # our so-called breadcrumb
    self.__local[funcName] = {}
    pointerVars = functionPointer[funcName]['vars']
    pointerTemps = functionPointer[funcName]['temps']
    arrParams = functionPointer[funcName]['arrParam']
    k = 0
    for i, j in pointerVars.items():
      if j.getIsParam():
        self.__local[funcName][j.getVirtualAddress()] = arrParams[k]
        k = k + 1
      else:
        self.__local[funcName][j.getVirtualAddress()] = None
    for i, j in pointerTemps.items():
      self.__local[funcName][j.getVirtualAddress()] = None
    self.__local[funcName]["goHere"] = goHere
    self.__localArr.append(self.__local[funcName])
    return

  def setConstants(self, dirFunc):
    consts = dirFunc["global"]["consts"] 
    for i, j in consts.items():
      if len(j) > 2000:
        raise Exception("ERROR! Too many variables!")  
      for k, l in j.items():
        self.__constants[l] = k

  @classmethod
  def instantiate(cls):
    if MainMemory.isAlive is None:
      MainMemory()
    return MainMemory.isAlive

  def reset(self):
    self.__global = {}
    self.__local = {}
    self.localMem = CallStackMemory()
    self.__localArr = []
    self.__constants = {}
    self.__classes = {}
    self.__pointer = None

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
  