from vm import VM, MainMemory
from symbolTable import SymbolTable, Variable
from quad import Quad
from jumps import Jumps
from plyler import lexer, parser, resetGlobals

symbolTable = SymbolTable.instantiate()
quadruple = Quad.instantiate()
jumps = Jumps.instantiate()
pointer = None

while True:
  # tok = lexer.token()
  # if not tok:
  #   break
  # print(tok)
    try:
      reading = input('Name of file > ')
      correct = reading
      correctFile = open(correct, 'r')
      curr = correctFile.read()
      correctFile.close()
      if parser.parse(curr) == 'SUCCESS':
        print("SUCCESSFULLY COMPILED!")
        print("---BEGINNING EXECUTION---") # a.out
        # symbolTable.printingAll()

        dirs = symbolTable.buildForVM()
        virtualMachine = VM(quadruple.quads, dirs[0], dirs[1])
        
        # start main memory
        MainMemory.instantiate()

        virtualMachine.execute()
      # quadruple.print()
      # symbolTable.buildSkeleton()
      symbolTable.reset()
      quadruple.reset()
      resetGlobals()

    except EOFError:
      print("INCORRECT")
    if not reading: continue
