# global variable to instantiate only ONCE
class Variable:
  def __init__(self, varName, varType, dimensions, isParam):
    self.__varName = varName
    self.__varType = varType
    self.__dimensions = dimensions
    self.__isParam = isParam
    self.__value = None

  # getters
  def getVarName(self):
    return self.__varName
  
  def getVarType(self):
    return self.__varType

  def getDimensions(self):
    return self.__dimensions

  def getValue(self):
    return self.__value

  def getIsParam(self):
    return self.__isParam

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
    return "{\n name: %s \n type: %s \n dimensions: %s \n value: %s \n isParam: %s \n}" % (self.getVarName(), self.getVarType(), self.getDimensions(), self.getValue(), self.getIsParam())

class Scope:
  # SCOPE: what a block contains.
  # Global scopes contain variables, functions, and classes
  # Class local scopes contain variables and functions (empty scopeClasses objects)
  # Function local scopes contain variables (empty scopeFunctions and scopeClasses objects)

  def __init__(self, type, context):
    self.__scopeType = type # Will be used to validate if local or global
    self.__context = context
    self.__scopeFunctions = {}
    self.__scopeVariables = {}
    self.__scopeClasses = {}
    self.__latestName = None
    self.__latestType = None
    self.__latestExpValue = None
    self.__latestDimension = 0

  # getters
  def getScopeType(self):
    return self.__scopeType

  def getContext(self):
    return self.__context

  def getScopeVariables(self):
    return self.__scopeVariables

  def getScopeFunctions(self):
    return self.__scopeFunctions

  def getScopeClasses(self):
    return self.__scopeClasses

  def getLatestName(self):
    return self.__latestName

  def getLatestType(self):
    return self.__latestType 

  def getLatestDimension(self):
    return self.__latestDimension 

  def getLatestExpValue(self):
    return self.__latestExpValue 

  # setters
  def setScopeType(self, scopeType):
    self.__scopeType = scopeType

  def setContext(self, context):
    self.__context = context

  def setLatestName(self, latestName):
    self.__latestName = latestName

  def setLatestType(self, latestType):
    self.__latestType = latestType
           
  def setLatestDimension(self):
    self.__latestDimension += 1

  def resetLatestDimension(self):
    self.__latestDimension = 0

  def setLatestExpValue(self, val):
    self.__latestExpValue = val

  # methods
  def addVariable(self, varName, varType, dimensions, isParam):
    if varName in self.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'already exists!')
      # return False

    self.__scopeVariables[varName] = Variable(varName, varType, dimensions, isParam)
    self.resetLatestDimension()


  def addFunction(self, funcName, funcType):
    if funcName in self.getScopeFunctions():
      raise Exception('ERROR! Function with identifier: ', funcName, 'already exists!')
      # return False

    if (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'global'):
      keyword = 'function'
    elif (SymbolTable.instantiate().getCurrentScope().getScopeType() == 'class'):
      keyword = 'classFunction'
    else:
      keyword = 'function' # remove UnboundLocalError
    self.__scopeFunctions[funcName] = Scope(funcType, keyword)
    SymbolTable.instantiate().setCurrentScope(self.__scopeFunctions[funcName])
    
  def addClass(self, className):
    if className in self.getScopeClasses():
      raise Exception('ERROR! Class with identifier:', className, 'already exists!')
      # return False

    classType = 'class'
    self.__scopeClasses[className] = Scope(classType, classType)
    SymbolTable.instantiate().setStackPush(className)
    SymbolTable.instantiate().setCurrentScope(self.__scopeClasses[className])


  def sawCalledVariable(self, varName):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not varName in self.getScopeVariables() and not varName in globalScope.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'is not defined in this scope')
      # return False
    
    self.resetLatestDimension()
    if varName in self.getScopeVariables():
      return self.__scopeVariables[varName]
    elif varName in globalScope.getScopeVariables():
      return globalScope.__scopeVariables[varName]


  def doesClassExist(self, className, varName):
    globalScope = SymbolTable.instantiate().getGlobalScope()
    if not className in globalScope.getScopeClasses():
      raise Exception('ERROR! Class with identifier: ', className, 'is not defined in this scope')
      # return False
    
    currentClass = globalScope.__scopeClasses[className]

    if not varName in currentClass.getScopeVariables():
      raise Exception('ERROR! Variable with identifier:', varName, 'is not defined in this scope')
      # return False
    
    return currentClass.__scopeVariables[varName]


  def __repr__(self):
    return "{\n type: %s \n context: %s \n}" % (self.getScopeType(), self.getContext())

class SymbolTable:
  isAlive = None

  def __init__(self):
    SymbolTable.isAlive = self
    self.__globalScope = {}
    keyword = "global"
    self.__globalScope["global"] = Scope(keyword, keyword)
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
    print(self.__classStack[-1])
    return self.__classStack[-1]

  def setCurrentScope(self, val):
    self.__currentScope = val

  def setCurrentScope(self, val):
    self.__currentScope = val

  def setStackPush(self, value):
    self.__classStack.append(value)
    print(self.__classStack[-1])

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
      print(self.getStack())
      self.setCurrentScope(self.__globalScope["global"].getScopeClasses()[self.getStack()])
    elif (self.getCurrentScope().getContext() == 'function'):
      self.setCurrentScope(self.__globalScope["global"])

  def exitClassScope(self):
    self.setCurrentScope(self.__globalScope["global"])

  def printingAll(self):
    for key, val in self.__globalScope.items():
      print(key, ': ', val)

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
    self.__globalScope["global"] = Scope(keyword, keyword)
    self.__currentScope = self.__globalScope["global"]
    self.__classStack = []

