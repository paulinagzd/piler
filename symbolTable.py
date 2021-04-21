class Variable:
    def __init__(self):
        self.name = None
        self.type = None
        self.value = None

class Function:
    def __init__(self):
        self.name = None
        self.type = None
        self.variableTable = {} 
    
    # Variable dictionary storing design -> variable_name : variable_object
    def addVariable(self,variableName):
        if variableName in self.variableTable.keys():
            print("Variable already declared")
        else:
            self.variableTable[variableName] = Variable()
    
    def getVariable(self,variableName):
        if variableName not in self.variableTable.keys():
            print("Variable doesn't exist")
        else:
            return self.variableTable[variableName]


    def setVariable(self,variableName,value):
        if variableName not in self.variableTable.keys():
            print("Variable doesn't exist")
        else:
            self.variableTable[variableName].value = value
        

class SymbolTable:
    def __init__(self):
        self.functionTable = {'global': Function()} # Symbol Table storage -> function_name : function_object
    
    def addFunction(self,functionName):
        if functionName in self.functionTable.keys():
            print("Function already declared")
        else:
            self.functionTable[functionName] = Function()
        
    def getFunction(self,functionName):
        if functionName not in self.functionTable.keys():
            print("Function doesn't exist")
        else:
            return self.variableTable[functionName]

    def deleteFunction(self,functionName):
        if self.functionTable:
            if function.name in self.functionTable.keys():
                del self.functionTable[functionName]
            else:
                print("Function doesn't exist")
        else:
            print("No functions declared")
