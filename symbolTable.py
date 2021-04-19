class Variable:
    def __init__(self,name,type,function):
        self.name = name
        self.type = type
        self.scope = [function.name]
        self.value = None

class Function:
    def __init__(self,name,type,parent):
        self.name = name
        self.type = type
        self.parent = parent # this can be a function object
        self.variableTable = {} 
    
    # Variable dictionary storing design -> variable_name : variable_object
    def addVariable(self,variable):
        if variable.name in self.variableTable.keys():
            print("Variable already declared")
        else:
            self.variableTable[variable.name] = variable
            if self.parent:
                self.variableTable[variable.name].scope
    
    def getVariable(self,variable):
        if variable.name not in self.variableTable.keys():
            print("Variable doesn't exist")
        else:
            return self.variableTable[variable.name]


    def setVariable(self,variable,value):
        if variable.name not in self.variableTable.keys():
            print("Variable doesn't exist")
        else:
            self.variableTable[variable.name].value = value
        

class SymbolTable:
    def __init__(self,programName):
        self.functionTable = {} # Symbol Table storage -> function_name : function_object
    
    def addFunction(self,function):
        if function.name in self.functionTable.keys():
            print("Function already declared")
        else:
            self.variableTable[function.name] = function
        
    def getFunction(self,function):
        if function.name not in self.functionTable.keys():
            print("Function doesn't exist")
        else:
            return self.variableTable[function.name]

    def deleteFunction(self,function):
        if self.functionTable:
            if function.name in self.functionTable.keys():
                del self.functionTable[function.name]
            else:
                print("Function doesn't exist")
        else:
            print("No functions declared")
