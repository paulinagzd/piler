from quad import Quad

quadruple = Quad.instantiate()

class VM:
    def __init__(self, quadList):
        self.__quadList = quadList
        self.__nextPointer = 1

    # Processing Operations
    def add(self):
        return False

    def subtract(self):
        return False

    def multiply(self):
        return False

    def divide(self):
        return False  

    def assign(self):
        return False

    def lt(self):
        return False
        
    def gt(self):
        return False
        
    def le(self):
        return False
        
    def ge(self):
        return False
        
    def equal(self):
        return False
        
    def notEqual(self):
        return False

    def printLine(self):
        return False

    def readLine(self):
        return False
        
    def goto(self):
        return False
        
    def gotoF(self):
        return False

    def gotoV(self):
        return False
        
    def goSub(self):
        return False

    #MAIN VM PROGRAM
    def driverProgram(self):
        operCode = quadList[nextPointer][0]
        while (operCode != 19):
            if operCode == 1: #sumar
                self.add()

            elif operCode == 2:
                self.subtract()

            elif operCode == 3:
                self.multiply()

            elif operCode == 4:
                self.divide()

            elif operCode == 5:
                self.assign()

            elif operCode == 6:
                self.lt()

            elif operCode == 7:
                self.gt()

            elif operCode == 8:
                self.le()

            elif operCode == 9:
                self.ge()

            elif operCode == 10:
                self.equal()

            elif operCode == 11:
                self.notEqual()

            elif operCode == 12:
                self.printLine()

            elif operCode == 13:
                self.readLine()
            
            elif operCode == 14:
                self.goto()
            
            elif operCode == 15:
                self.gotoF()
            
            elif operCode == 16:
                self.gotoV()
            
            elif operCode == 17:
                self.goSub()

            elif operCode == 18:
                self.endFunc()
        