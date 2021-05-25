from vm import VM
from symbolTable import SymbolTable
from quad import Quad
from jumps import Jumps
from plyler import lexer, parser

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
        print("BEGGINING EXECUTION...") # a.out
        virtualMachine = VM(quadruple.quads)
      # symbolTable.printingAll()
      quadruple.print()
      symbolTable.reset()
      quadruple.reset()

    except EOFError:
      print("INCORRECT")
    if not reading: continue
