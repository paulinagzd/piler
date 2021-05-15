class Memory:
    def __init__(self):
        self.__funcName = None
        self.__global = {
            'int':[],
            'flt':[],
            'boo':[],
            'cha':[],
            'str':[],
        }
        self.__local = {
            'int':[],
            'flt':[],
            'boo':[],
            'cha':[],
            'str':[],
        }

    def setGlobal(self, var):
        self.__global[var.getVarType].append(var.getValue)
        dir = len(self.__global[var.getVarType]) - 1
        var.setDir(dir)

    def setLocal(self, var):
        self.__local[var.getVarType].append(var.getValue)
        dir = len(self.__local[var.getVarType]) - 1
        var.setDir(dir)
    
    def setFuncName(self, funcName):
        self.__funcName = funcName

    def getVar(self, var):
        return self.__global[var.getVarType][var.getDir]
    
    def getTmp(self, var):
        return self.__local[var.getVarType][var.getDir]
    
    def getFuncName(self):
        return self.__funcName