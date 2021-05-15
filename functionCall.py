import memory

class FunctionCall:
    def __init__(self,funcName):
        self.__memory = memory.Memory(funcName)
