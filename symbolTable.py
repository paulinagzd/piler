from quad import Quad
from vm import MemoryContainer
quadruple = Quad.instantiate()

cont = 0
cont2 = 0
class DimensionNode:
  def __init__(self, dim, lim):
    self.__dim = dim
    self.__mDim = None
    self.__lim = lim
    self.__offset = 0
    self.__content = []

  def getDim(self):
    return self.__dim

  def getLim(self):
    return self.__lim

  def getMDim(self):
    return self.__mDim

  def getOffset(self):
    return self.__offset

  def getVirtualAddress(self):
    return self.__virtualAddress

  def getContent(self):
    return self.__content

  def setMDim(self, val):
    self.__mDim = val
  
  def setOffset(self, val):
    self.__offset = val

  def __repr__(self):
    return "lSup: %s mDim = %s" % (self.__lim, self.__mDim)
class Variable:
  def __init__(self, varName, varType, dimensions, dimensionNodes, offset, isParam, memPointer, isObject):
    self.__varName = varName
    self.__varType = varType
    self.__dimensions = dimensions
    self.__dimensionNodes = dimensionNodes
    self.__isParam = isParam
    self.__virtualAddress = memPointer.getInitialAddress() + memPointer.getOffset()
    self.__isObject = isObject
    self.__value = None
    self.__memPointer = memPointer
    self.__offset = offset
    self.__value = None

    # incrementing offset when variable is created in memory
    # if dimensions > 0:
    #   memPointer.setDimensionalOffset(int(offset))
    # el
    if varName == '':
      pass
    else:  
      memPointer.setOffset()

  # getters
  def getVarName(self):
    return self.__varName
  
  def getVarType(self):
    return self.__varType

  def getDimensions(self):
    return self.__dimensions

  def getDimensionNodes(self):
    return self.__dimensionNodes

  def getValue(self):
    return self.__value

  def getIsParam(self):
    return self.__isParam

  def getVirtualAddress(self):
    return self.__virtualAddress

  def getIsObject(self):
    return self.__isObject

  def getOffset(self):
    return self.__offset

  def getMemPointer(self):
    return self.__memPointer

  # setters
  def setVarName(self, varName):
    self.__varName = varName

  def setVarType(self, varType):
    self.__varType = varType
  
  def setDimensions(self):
    self.__dimensions += 1

  def setValue(self, value):
    self.__value = value

  def setIsParam(self, value):
    self.__isParam = value

  def setIsObject(self, value):
    self.__isObject = value

  def setValue(self, value):
    self.__value = value

  def __repr__(self):
    if self.__dimensions > 0:
      return "{\n name: %s \n type: %s \n dimensions: %s array: %s \n value: %s \n isParam: %s \n virtualAddress: %s \n}" % (self.getVarName(), self.getVarType(), self.getDimensions(), self.getDimensionNodes(), self.getValue(), self.getIsParam(), self.__virtualAddress)
    else:
      return "{\n name: %s \n type: %s \n dimensions: %s \n value: %s \n isParam: %s \n virtualAddress: %s \n}" % (self.getVarName(), self.getVarType(), self.getDimensions(), self.getValue(), self.getIsParam(), self.__virtualAddress)

class Scope:
  # SCOPE: what a block contains.
  # Global scopes contain variables, functions, and classes
  # Class local scopes contain variables and functions (empty scopeClasses objects)
  # Function local scopes contain variables (empty scopeFunctions and scopeClasses objects)

  def __init__(self, type, name, context, starts):
    self.__scopeType = type # Will be used to validate if local or global
    self.__scopeName = name
    self.__context = context
    self.__scopeFunctions = {}
    self.__scopeVariables = {}
    self.__scopeClasses = {}
    self.__scopeConstants = {}
    self.__scopeTemps = {}
    self.__latestName = None
    self.__latestFuncName = None
    self.__latestType = None
    self.__latestExpValue = None
    self.__latestDimension = 0
    self.__r = 1
    self.starts = starts
    # for functions and modules
    self.__quadCont = 0
    self.__numParams = 0
    self.__numLocalVars = 0
    self.__latestReturnValue = None
    self.__currentFunctionParams = []
    self.__temps = {
      'int' : 0,
      'ints': 0,
      'flt' : 0,
      'flts': 0,
      'boo' : 0,
      'boos': 0,
      'cha' : 0,
      'chas': 0,
      'str' : 0,
      'strs': 0,
    }
    self.__dimensionNodes = []
    self.__matchingParams = False

    if type == 'global' or type == 'class':
      self.memory = MemoryContainer(type)

  # getters
  def getScopeType(self):
    return self.__scopeType

  def getScopeName(self):
    return self.__scopeName

  def getContext(self):
    return self.__context

  def getScopeVariables(self):
    return self.__scopeVariables

  def getScopeFunctions(self):
    return self.__scopeFunctions

  def getScopeClasses(self):
    return self.__scopeClasses

  def getScopeConstants(self):
    return self.__scopeConstants

  def getScopeTemps(self):
    return self.__scopeTemps

  def getLatestName(self):
    return self.__latestName

  def getLatestFuncName(self):
    return self.__latestFuncName

  def getLatestType(self):
    return self.__latestType 

  def getLatestDimension(self):
    return self.__latestDimension 

  def getLatestExpValue(self):
    return self.__latestExpValue 

  def getQuadCont(self):
    return self.__quadCont 

  def getNumParams(self):
    return self.__numParams 

  def getNumLocalVars(self):
    return self.__numLocalVars 

  def getCurrentFunctionParams(self):
    return self.__currentFunctionParams 

  def getLatestReturnValue(self):
    return self.__latestReturnValue

  def getTemps(self):
    return self.__temps
    
  def getMatchingParams(self):
    return self.__matchingParams

  # setters
  def setScopeType(self, scopeType):
    self.__scopeType = scopeType

  def setContext(self, context):
    self.__context = context

  def setLatestName(self, latestName):
    self.__latestName = latestName

  def setLatestFuncName(self, val):
    self.__latestFuncName = val

  def setLatestType(self, latestType):
    self.__latestType = latestType
           
  def setLatestDimension(self, lim):
    self.__latestDimension = self.__latestDimension + 1
    if lim != -1:
      self.__r = lim * self.__r
      # print("ADDING DIM", self.__latestDimension, lim, temp)
      self.__dimensionNodes.append(DimensionNode(self.__latestDimension, lim))

  def resetLatestDimension(self):
    self.__latestDimension = 0

  def setLatestExpValue(self, val):
    self.__latestExpValue = val

  def setQuadCont(self, val):
    self.__quadCont = val

  def setNumParams(self, val):
    self.__numParams = val

  def setNumLocalVars(self, val):
    self.__numLocalVars = val

  def setCurrentFunctionParams(self, val):
    self.__currentFunctionParams.append(val)

  def clearCurrentFunctionParams(self):
    self.__currentFunctionParams = []
    
  def setLatestReturnValue(self):
    self.__latestReturnValue = self.__latestExpValue

  def setTemps(self, key, val):
    self.__temps[key] = val

  def findConstVA(self, val):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if val in globalScope.getScopeConstants():
      return globalScope.getScopeConstants()[val].getVirtualAddress()
      
  def setMatchingParams(self, val):
    self.__matchingParams = val

  def getTypeConstants(self, operand):
    if isinstance(operand,float):
      return 'flt'
    elif isinstance(operand,int):
      return 'int'
    elif isinstance(operand, str):
      if len(operand) == 3 and operand[0] == '\'':
        return 'cha'
      else:
        return 'str'

  # methods
  def verifyArrContent(self, array, varType, dimensions, dimensionNodes):
    newVarType = varType
    if varType[-1] == 's':
      newVarType = varType[:3]

    # print("LEN ARRAY", len(array))
    if len(array) == 1 and len(array) != dimensions:
      raise Exception('ERROR! Variable with incorrect dimensions')
    else:
      if dimensions == 2:
        arrSize1 = dimensionNodes[0].getLim()
        arrSize2 = dimensionNodes[1].getLim()
        for i in array:
          if len(i) != arrSize2:
            raise Exception('ERROR! Variable with incorrect dimensions')
            for j in i:
              if len(j) != arrSize1:
                raise Exception('ERROR! Variable with incorrect dimensions')                      
              if self.getTypeConstants(j) != newVarType:
                raise Exception('ERROR! Variable with incorrect type for dimensions')
      else:
        for j in array[0]:
          if self.getTypeConstants(j) != newVarType:
            raise Exception('ERROR! Variable with incorrect type for dimensions')
    return True

  def addVariableWithDimensions(self, varName, varType, dimensions, dimNodes, offset, isParam, memPointer, isObject, contP, flatList):
    temp = 0
    while temp < len(flatList):
      if temp == 0:
        self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, isObject)
        self.__scopeVariables[varName].setValue(flatList[temp])
      else:
        varName = strObj = str(int(offset))
        self.__scopeVariables[varName + strObj] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, isObject)
        self.__scopeVariables[varName + strObj].setValue(flatList[temp])
      temp += 1
      # offset -= 1


  def addVariable(self, varName, varType, dimensions, isParam, varDim):
    if varName in self.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'already exists!')

    # if it has dimensions it needs to complete the dimensionNodes
    offset = 0
    if dimensions > 0:
      for dimNode in self.__dimensionNodes:
        mDim = self.__r / (dimNode.getLim())

        self.__r = int(mDim)
        dimNode.setMDim(int(mDim))
      self.__r = 1
    # adding the variable depending on the scope it's in, considering classes as global and local memory
    if self.__context == 'global' or self.__context == 'class':
      memPointer = self.memory.memSpace['global'][varType]['real']
      isObject = True if self.__context == 'class' else False
      if dimensions > 0 and self.verifyArrContent(varDim, varType, dimensions, self.__dimensionNodes):
        temp = 0
        flatList = [item for sublist in varDim for item in sublist]
        while temp < len(flatList):
          if temp == 0:
            self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, isObject)
            self.__scopeVariables[varName].setValue(flatList[temp])
          else:
            strObj = str(int(temp))
            self.__scopeVariables[varName + strObj] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, isObject)
            self.__scopeVariables[varName + strObj].setValue(flatList[temp])
          temp += 1
      else:
        self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, isObject)
    elif SymbolTable.instantiate().getCurrentScope().getContext() == 'function' or SymbolTable.instantiate().getCurrentScope().getContext() == 'classFunction':
      globalScope = SymbolTable.instantiate().getGlobalScope()
      if SymbolTable.instantiate().getCurrentScope().getContext() == 'function':
        # store in global's memory
        memPointer = globalScope.memory.memSpace['local'][varType]['real']
      else:
        classScope = globalScope.getScopeClasses()[SymbolTable.instantiate().getStack()]
        memPointer = classScope.memory.memSpace['local'][varType]['real']
      if dimensions > 0 and self.verifyArrContent(varDim, varType, dimensions, self.__dimensionNodes):
        temp = 0
        flatList = [item for sublist in varDim for item in sublist]
        while temp < len(flatList):          
          if temp == 0:
            self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, False)
            self.__scopeVariables[varName].setValue(flatList[temp])
          else:
            self.__scopeVariables[varName + str(temp)] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, False)
            self.__scopeVariables[varName + str(temp)].setValue(flatList[temp])
          temp += 1
      else:
        self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer, False)
    else:
      #TODO for CLASSES AND OBJECTS
      pass
    self.__dimensionNodes = []
    self.resetLatestDimension()

  # addConstant
  # What: adds constant values with virtual memory address to Constant class
  # Parameters: The value and data type of this constant
  # Returns an updated __scopeConstants object for the global scope/whole program
  # When is it used: Every time a constant value is read on the sample programs
  def addConstant(self, value, type):
    globalScope = SymbolTable.instantiate().getGlobalScope()

    if type in globalScope.getScopeConstants():
      constantTypePointer = globalScope.__scopeConstants[type]
      if not value in constantTypePointer:
        memPointer = globalScope.memory.memSpace['constants'][type]
        constantTypePointer[value] = memPointer.getInitialAddress() + memPointer.getOffset()
        memPointer.setOffset()
    else:
      globalScope.__scopeConstants[type] = {}
      constantTypePointer = globalScope.__scopeConstants[type]
      memPointer = globalScope.memory.memSpace['constants'][type]
      constantTypePointer[value] = memPointer.getInitialAddress() + memPointer.getOffset()
      memPointer.setOffset()

  def addFunction(self, funcName, funcType):
    if funcName in self.getScopeFunctions():
      raise Exception('ERROR! Function with identifier: ', funcName, 'already exists!')

    if (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'global'):
      keyword = 'function'
    elif (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'class'):
      keyword = 'classFunction'
    else:
      keyword = 'function' # remove UnboundLocalError
    self.__scopeFunctions[funcName] = Scope(funcType, funcName, keyword, quadruple.quadCounter)
    SymbolTable.instantiate().setCurrentScope(self.__scopeFunctions[funcName])
    
  def addClass(self, className):
    if className in self.getScopeClasses():
      raise Exception('ERROR! Class with identifier:', className, 'already exists!')

    classType = 'class'
    self.__scopeClasses[className] = Scope(classType, className, classType, -1)
    SymbolTable.instantiate().setStackPush(className)
    SymbolTable.instantiate().setCurrentScope(self.__scopeClasses[className])

  def sawCalledVariable(self, varName):
    globalScope = SymbolTable.instantiate().getGlobalScope()

    if not varName in self.getScopeVariables() and not varName in globalScope.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'is not defined in this scope')
    
    if varName in self.getScopeVariables():
      return self.__scopeVariables[varName]
    elif varName in globalScope.getScopeVariables():
      return globalScope.__scopeVariables[varName]
    self.resetLatestDimension()

  def sawCalledFunction(self, funcName, scope, className):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    pointer = globalScope
    if scope == 'class':
      if not funcName in globalScope.getScopeClasses()[className].getScopeFunctions():
        raise Exception('ERROR! FUNCTION with identifier:', funcName, 'is not defined in this program')
      else:
        pointer = globalScope.getScopeClasses()[className]
    else:
      if not funcName in globalScope.getScopeFunctions() and self.__context == 'classFunction':
        # might be in a class
        pointer = globalScope.getScopeClasses()[SymbolTable.instantiate().getStack()]
      else:
        if funcName in globalScope.getScopeFunctions():
          pass
        else:
          raise Exception('ERROR! FUNCTION with identifier:', funcName, 'is not defined in this program')
    
    # print("GENERATE ERA", funcName, scope, pointer)
    if scope == 'class': 
      quadruple.saveQuad('era', funcName, scope, pointer.getScopeName())
    else:
      quadruple.saveQuad('era', funcName, scope, -1)
    functionParams = pointer.getScopeFunctions()[funcName].__scopeVariables
    self.setMatchingParams(True)
    for item, val in functionParams.items():
      if val.getIsParam():
        self.setCurrentFunctionParams(val)
      
    self.__latestFuncName = funcName
    return pointer.getScopeFunctions()[funcName]

  def doesClassExist(self, className, idName, type):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not className in globalScope.getScopeClasses():
      raise Exception('ERROR! Class with identifier: ', className, 'is not defined in this scope')
    
    currentClass = globalScope.__scopeClasses[className]
    if type == 'var':
      if not idName in currentClass.getScopeVariables():
        raise Exception('ERROR! Variable with identifier:', idName, 'is not defined in the class')
      return currentClass.__scopeVariables[idName]
    else:
      if not idName in currentClass.getScopeFunctions():
        raise Exception('ERROR! Function with identifier:', idName, 'is not defined in the class')
      return currentClass.__scopeName # returns class name

  def verifyDim(self, varName):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not varName in self.__scopeVariables and not varName in globalScope.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'is not defined in this scope')

    if varName in self.__scopeVariables:
      varPointer = self.__scopeVariables
    elif varName in globalScope.getScopeVariables():
      varPointer = globalScope.getScopeVariables()

    if varPointer[varName].getDimensions() == 0:
      raise Exception('ERROR! Variable with identifier:', varName, 'is one dimensional')
  
    return varPointer[varName]

  def countVars(self):
    for item, val in self.__scopeVariables.items():
      if val.getIsParam():
        self.__numParams += 1
      else :
        self.__numLocalVars += 1
    
    self.__quadCont = quadruple.quadCounter

  def __repr__(self):
    return "{\n starts :%s type: %s \n context: %s \n name: %s \n vars: %s \n}" % (self.starts, self.getScopeType(), self.getContext(), self.__scopeName, self.__scopeVariables)

class SymbolTable:
  isAlive = None

  def __init__(self):
    SymbolTable.isAlive = self
    self.__globalScope = {}
    keyword = "global"
    self.__globalScope["global"] = Scope(keyword, keyword, keyword, 1)
    self.__currentScope = self.__globalScope["global"]
    self.__classStack = []

  @classmethod
  def instantiate(cls):
    if SymbolTable.isAlive is None:
      SymbolTable()
    return SymbolTable.isAlive

  def getCurrentScope(self):
    return self.__currentScope

  def getGlobalScope(self):
    return self.__globalScope["global"]

  def getStack(self):
    return self.__classStack[-1]

  def setCurrentScope(self, val):
    self.__currentScope = val

  def setStackPush(self, value):
    self.__classStack.append(value)

  def setStackPop(self,):
    self.__classStack.pop()

  def addFunctionScope(self):
    current = self.getCurrentScope()
    current.addFunction(self.__currentScope.getLatestName(), self.__currentScope.getLatestType())

  def addClassScope(self):
    current = self.getCurrentScope()
    self.setStackPush(current.getLatestName())
    current.addClass(current.getLatestName())

  # if its in a local function, exit to global scope
  # if its in a class local, exit to global scope
  # if its in a class function, exit to local class
  def exitScope(self):
    if (self.getCurrentScope().getContext() == 'classFunction'):
      self.setCurrentScope(self.__globalScope["global"].getScopeClasses()[self.getStack()])
    elif (self.getCurrentScope().getContext() == 'function'):
      self.setCurrentScope(self.__globalScope["global"])
    temps = self.getCurrentScope().memory.memSpace["local"]
    for i, j in temps.items():
      j['real'].resetOffset()
      j['temp'].resetOffset()

  def exitClassScope(self):
    self.setCurrentScope(self.__globalScope["global"])

  def printingAll(self):
    for key, val in self.__globalScope.items():
      print(key, ': ', val)

      print('\n \n GLOBAL CONSTANTS')
      for aaa, aaaa in val.getScopeConstants().items():
        print(aaa, ': ', aaaa)

      print('\n \n GLOBAL VARIABLES')
      for i, ii in val.getScopeVariables().items():
        print(i, ': ', ii)

      print('\n \n GLOBAL TEMPS')
      print(len(val.getScopeTemps()))

      print('\n \n GLOBAL FUNCTIONS')
      for j, jj in val.getScopeFunctions().items():
        print(j, ': ', jj)

        print('\n \n FUNCTION VARIABLES')
        for m, mm in jj.getScopeVariables().items():
          print(m, ': ', mm)

        print('\n \n FUNCTION TEMPS')
        print(len(jj.getScopeTemps()))
        print('---------------------------------')

      print('\n \n CLASSES')
      for k, kk in val.getScopeClasses().items():
        print(k, ': ', kk)

        print('\n \n CLASS VARS')
        for n, nn in kk.getScopeVariables().items():
          print(n, ': ', nn)

        print('\n \n CLASS FUNCTIONS')
        for o, oo in kk.getScopeFunctions().items():
          print(o, ': ', oo)
        
          for x, xx in oo.getScopeVariables().items():
            print(x, ': ', xx)

          print('\n \n CLASS FUNC TEMPS')
          print(len(oo.getScopeTemps()))
          print('---------------------------------')
  
  def getFuncSize(self, func):
    res = {
      "local": {}, 
      "temps": {},  
    }

    for i, j in func.getScopeVariables().items():
      varType = j.getVarType()
      if not varType in res["local"]:
        # print("OFFSET", int(j.getOffset()))
        res["local"][varType] = int(j.getOffset()) + 1
      else:
        res["local"][varType] = int(res["local"][varType] + j.getOffset() + 1)
    for i, j in func.getScopeTemps().items():
      varType = j.getVarType()
      if not varType in res["temps"]:
        res["temps"][varType] = 1
      else:
        res["temps"][varType] += 1

    return res

  def buildForVM(self):
    res = []
    tempDirFunc = {"global": {
      "vars": self.getGlobalScope().getScopeVariables(),
      "temps": self.getGlobalScope().getScopeTemps(),
      "consts": self.getGlobalScope().getScopeConstants(),
      "funcs": {}
    }}

    tempArr = []
    tempDirClass = {
      "global": {}
    }

    pointer = tempDirFunc["global"]
    for key, val in self.__globalScope.items():
      # functions
      pointer = pointer["funcs"]
      for key1, val1, in val.getScopeFunctions().items():
        size = self.getFuncSize(val.getScopeFunctions()[key1])

        pointer[key1] = {
          "type": val1.getScopeType(),
          "size": size,
          "start": val1.starts,
          "vars": val1.getScopeVariables(),
          "temps": val1.getScopeTemps(),
        }
        # print(key1, pointer[key1])

      # classes are their own "world" inside the global scope
      # meaning they have global variables and dirFunc
      for key2, val2, in val.getScopeClasses().items():
        tempArr.append({key2: tempDirClass})
        pointer = tempArr[-1]
        pointer = pointer[key2]["global"]
        pointer["vars"] = val2.getScopeVariables(),
        pointer["funcs"] = {}
        pointer = pointer["funcs"]
        for keyClass, valClass, in val2.getScopeFunctions().items():
          size = self.getFuncSize(val2.getScopeFunctions()[keyClass])
          pointer[keyClass] = {
            "type": valClass.getScopeType(),
            "size": size,
            "start": valClass.starts,
            "vars": valClass.getScopeVariables(),
            "temps": valClass.getScopeTemps(),
          }
          # print(keyClass, pointer[keyClass])

    # print("ENTRO")
    # print("DIRFUNC")
    # for i, j in tempDirFunc.items():
    #   print(tempDirFunc[i])
    # print("DIRCLASS")
    # for i, j in tempDirClass.items():
    #   print(tempDirClass[i])
  
    res.append(tempDirFunc)
    res.append(tempArr)
    return res

  def reset(self):
    self.__globalScope = {}
    keyword = "global"
    self.__globalScope["global"] = Scope(keyword, keyword, keyword, 1)
    self.__currentScope = self.__globalScope["global"]
    self.__classStack = []
