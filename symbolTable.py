from semanticCube import SemanticCube
from quadForms import QuadForms

# global variable to instantiate only ONCE
s = None
class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.value = None

    def setValue(self, value):
        self.value = value

    def setType(self, type):
        self.type = type

    # def __repr__(self):
    #     return "<VARIABLE with type %s value %s> \n" % (self.type, self.value)    # def __str__(self):
    
    # def __str__(self):
    #    return "<VARIABLE with type %s value %s> \n" % (self.type, self.value)

    # def print(self):
    #     for item in self.getScopeVariables():
    #         item.printV()
class Function:
    def __init__(self, name, type, varTable):
        self.name = name
        self.type = type
        self.variableTable = varTable


    # def __repr__(self):
    #     return "<FUNCTION with type %s varTable %s> \n" % (self.type, self.variableTable) 
    
    
    # def __str__(self):
    #     return "<FUNCTION with type %s varTable %s> \n" % (self.type, self.variableTable) 
        
    def getVariableTable(self):
        return self.variableTable
        
class Scope:
    def __init__(self, scopeId):
        self.scopeId = scopeId
        self.scopeVariables = {}
        self.scopeFunctions = {}

    def getScopeId(self):
        return self.scopeId

    def getScopeVariables(self):
        return self.scopeVariables

    def getScopeFunctions(self):
        return self.scopeFunctions

    def addVariable(self, varId, varType, value):
        if varId not in self.scopeVariables:
            self.scopeVariables[varId] = Variable(varId, varType)
        else:
            print("Variable already declared")
            self.scopeVariables[varId].setValue(value)
            # return False

    def addClass(self, classId, classType):
        if classId not in self.scopeFunctions:
            self.scopeFunctions[classId] = { classId : Scope(classId) }
            s.getInstance().setLatestScope(self.scopeFunctions[classId][classId])
            # for item in self.getScopeVariables().items():
            #     print(item)
        else:
            print("Function already declared")
            return False

    def addFunction(self, functionId, functionType):
        if functionId not in self.scopeFunctions:
            self.scopeFunctions[functionId] = Function(functionId, functionType, { functionId : Scope(functionId) })
            s.getInstance().setLatestScope(self.scopeFunctions[functionId].getVariableTable()[functionId])
            # for item in self.getScopeFunctions().items():
            #     print(item)
        else:
            print("Function already declared")
            return False

    # def __repr__(self):
    #     return "%s SCOPE : %s %s > \n" % (self.scopeId, self.scopeFunctions, self.scopeVariables)    # def __str__(self):
    
    # def __str__(self):
    #     return "%s SCOPE : %s %s > \n" % (self.scopeId, self.scopeFunctions, self.scopeVariables)    # def __str__(self):

    # def print(self):
    #     for item in self.getScopeVariables():
    #         print(item)
    #     for item in self.getScopeFunctions():
    #         print(item)

class SymbolTable:
    def __init__(self):
        self.functionTable = {} # Symbol Table storage -> function_name : function_object
        self.allScopes = None
        self.context = None
        self.latestType = None
        self.latestId = None
        self.latestValue = []
        self.latestOps = []
        self.latestFunction = None
        self.__latestScope = None
        self.globalScopeObject = None
        global s 
        s = self

    def getInstance(self):
        return self

    def getLatestScope(self):
        return self.__latestScope

    def setLatestScope(self, x):
        self.__latestScope = x
        # print('latestScope', self.__latestScope)

    def getLatestFunction(self):
        return self.__latestScope

    def instantiate(self):
        self.allScopes = { self.latestId : Scope(self.latestId) }
        self.globalScope = self.allScopes[self.latestId]
        self.setLatestScope(self.globalScope)

    def scopeStarts(self):
        print('entreScopeStart', self.__latestScope)

    def scopeEnds(self):
        print('entreScopeEnds next line cambio')
        self.setLatestScope(self.globalScope)

    def addLatestVariable(self):
        # print('variable:', self.latestId, self.latestType, self.getLatestScope())
        self.getLatestScope().addVariable(self.latestId, self.latestType, None)

    def addLatestVariableValue(self, value):
        # print('variable:', self.latestId, self.latestType, self.getLatestScope())
        self.getLatestScope().addVariable(self.latestId, self.latestType, value)

    def addLatestParameterVariable(self):
        # print('param:', self.latestId, self.latestType, self.getLatestScope())
        self.getLatestScope().addVariable(self.latestId, self.latestType, None)

    def addLatestClass(self):
        # print('class:', self.latestId, self.latestType)
        self.getLatestScope().addClass(self.latestId, self.latestType)

    def addLatestFunction(self):
        # print('function:', self.latestId, self.latestType)
        self.getLatestScope().addFunction(self.latestId, self.latestType)

    def addLatestValues(self, value, type, stack):
        # print(stack)
        if stack == 'pilao':
            self.latestValue.append({"value": value, "type": type})
        else:
            self.latestOps.append(value)
            # if self.latestOps.top() == '+' or self.latestOps.top() == '-'
                # generateQuad

    def assignOperation(self):
        print(self.latestId)
        print(self.getLatestScope())
        print('entro lv')
        for item in self.latestValue:
            print(item)
        self.latestValue = []

        print('entro lops')
        for item in self.latestOps:
            print(item)
        self.latestOps = []

        lsc = self.getLatestScope().getScopeVariables()[self.latestId].type
        print(lsc)

        # SemanticCube.quad(self.latestOps, self.latestValue, self.latestId)


    # def printScopes(self):
    #         # self.allScopes['viendo'].__repr__()
    #         for item in self.allScopes['viendo']:
    #             item.print()
