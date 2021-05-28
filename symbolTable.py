from quad import Quad
from vm import memSpace, MemSpaceContainer
quadruple = Quad.instantiate()

class DimensionNode:
  def __init__(self, dim, lim, temp):
    self.__dim = dim
    self.__r = (lim + 1) * temp
    self.__lim = lim
    self.__offset = 0

  def getDim(self):
    return self.__dim

  def getLim(self):
    return self.__lim

  def getR(self):
    return self.__r

  def getOffset(self):
    return self.__offset

  def setR(self, val):
    self.__r = val
  
  def setOffset(self, val):
    self.__offset = val

  def getVirtualAddress(self):
    return self.__virtualAddress

  def __repr__(self):
    return "lSup: %s m or k = %s" % (self.__lim, self.__r)
class Variable:
  def __init__(self, varName, varType, dimensions, dimensionNodes, offset, isParam, memPointer):
    self.__varName = varName
    self.__varType = varType
    self.__dimensions = dimensions
    self.__dimensionNodes = dimensionNodes
    self.__isParam = isParam
    self.__virtualAddress = memPointer.getInitialAddress() + memPointer.getOffset()
    self.__value = None

    # incrementing offset when variable is created in memory
    if dimensions > 0:
      memPointer.setDimensionalOffset(int(offset))
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

  def __repr__(self):
    if self.__dimensions > 0:
      return "{\n name: %s \n type: %s \n dimensions: %s array: %s \n value: %s \n isParam: %s \n virtualAddress: %s \n}" % (self.getVarName(), self.getVarType(), self.getDimensions(), self.getDimensionNodes(), self.getValue(), self.getIsParam(), self.__virtualAddress)
    else:
      return "{\n name: %s \n type: %s \n dimensions: %s \n value: %s \n isParam: %s \n virtualAddress: %s \n}" % (self.getVarName(), self.getVarType(), self.getDimensions(), self.getValue(), self.getIsParam(), self.__virtualAddress)

class ParameterTable:
  isAlive = None
  def __init__(self, params):
    isAlive = self
    self = params
class Scope:
  # SCOPE: what a block contains.
  # Global scopes contain variables, functions, and classes
  # Class local scopes contain variables and functions (empty scopeClasses objects)
  # Function local scopes contain variables (empty scopeFunctions and scopeClasses objects)

  def __init__(self, type, name, context):
    self.__scopeType = type # Will be used to validate if local or global
    self.__scopeName = name
    self.__context = context
    self.__scopeFunctions = {}
    self.__scopeVariables = {}
    self.__scopeClasses = {}
    self.__scopeConstants = {}
    self.__latestName = None
    self.__latestFuncName = None
    self.__latestType = None
    self.__latestExpValue = None
    self.__latestDimension = 0
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
      temp = 1 if self.__latestDimension == 1 else self.__dimensionNodes[0].getR()
      self.__dimensionNodes.append(DimensionNode(self.__latestDimension, lim, temp))

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

  # methods
  def addVariable(self, varName, varType, dimensions, isParam):
    if varName in self.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'already exists!')

    # if it has dimensions it needs to complete the dimensionNodes
    offset = 0
    if dimensions > 0:
      size = self.__dimensionNodes[0].getR()
      for dimNode in self.__dimensionNodes:
        mDim = dimNode.getR() / (dimNode.getLim() + 1)
        dimNode.setR(int(mDim))
        offset = offset + dimNode.getLim() * mDim
        dimNode.setOffset(int(offset))
      self.__dimensionNodes[-1].setR(0)

    # adding the variable depending on the scope it's in
    if SymbolTable.instantiate().getCurrentScope().getContext() == 'global':
      memPointer = memSpace['global'][varType]['real']
      self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer)
    elif SymbolTable.instantiate().getCurrentScope().getContext() == 'function':
      memPointer = memSpace['local'][varType]['real']
      self.__scopeVariables[varName] = Variable(varName, varType, dimensions, self.__dimensionNodes, offset, isParam, memPointer)
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
        memPointer = memSpace['constants'][type]
        constantTypePointer[value] = memPointer.getInitialAddress() + memPointer.getOffset()
        memPointer.setOffset()
    else:
      globalScope.__scopeConstants[type] = {}
      constantTypePointer = globalScope.__scopeConstants[type]
      memPointer = memSpace['constants'][type]
      constantTypePointer[value] = memPointer.getInitialAddress() + memPointer.getOffset()
      memPointer.setOffset()

  def addTemp(self, type, value):
    memPointer = memSpace['local'][type]['temp']
    memPointer[value] = {"TODO VALOR TEMP AQUI"}

  def addFunction(self, funcName, funcType):
    if funcName in self.getScopeFunctions():
      raise Exception('ERROR! Function with identifier: ', funcName, 'already exists!')

    if (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'global'):
      keyword = 'function'
    elif (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'class'):
      keyword = 'classFunction'
    else:
      keyword = 'function' # remove UnboundLocalError
    self.__scopeFunctions[funcName] = Scope(funcType, funcName, keyword)
    SymbolTable.instantiate().setCurrentScope(self.__scopeFunctions[funcName])
    
  def addClass(self, className):
    if className in self.getScopeClasses():
      raise Exception('ERROR! Class with identifier:', className, 'already exists!')

    classType = 'class'
    self.__scopeClasses[className] = Scope(classType, className, classType)
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

    self.resetLatestDimension()

  def sawCalledFunction(self, funcName):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not funcName in globalScope.getScopeFunctions():
      raise Exception('ERROR! FUNCTION with identifier:', funcName, 'is not defined in this program')
    
    quadruple.saveQuad('era', funcName, -1, -1)

    functionParams = globalScope.__scopeFunctions[funcName].__scopeVariables
    self.setMatchingParams(True)
    for item, val in functionParams.items():
      if val.getIsParam():
        self.setCurrentFunctionParams(val)
      
    self.__latestFuncName = funcName
    return globalScope.__scopeFunctions[funcName]

  def doesClassExist(self, className, varName):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not className in globalScope.getScopeClasses():
      raise Exception('ERROR! Class with identifier: ', className, 'is not defined in this scope')
    
    currentClass = globalScope.__scopeClasses[className]

    if not varName in currentClass.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'is not defined in this scope')
    
    return currentClass.__scopeVariables[varName]

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
    return "{\n type: %s \n context: %s \n}" % (self.getScopeType(), self.getContext())

class SymbolTable:
  isAlive = None

  def __init__(self):
    SymbolTable.isAlive = self
    self.__globalScope = {}
    keyword = "global"
    self.__globalScope["global"] = Scope(keyword, keyword, keyword)
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

    temps = memSpace["local"]
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

      print('\n \n GLOBAL FUNCTIONS')
      for j, jj in val.getScopeFunctions().items():
        print(j, ': ', jj)

        print('\n \n FUNCTION VARIABLES')
        for m, mm in jj.getScopeVariables().items():
          print(m, ': ', mm)
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
          print('---------------------------------')
  
  def reset(self):
    self.__globalScope = {}
    keyword = "global"
    self.__globalScope["global"] = Scope(keyword, keyword, keyword)
    self.__currentScope = self.__globalScope["global"]
    self.__classStack = []

