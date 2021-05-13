from symbolTable import SymbolTable
from quad import Quad
from jumps import Jumps
from pi_lex_yacc import piser

symbolTable = SymbolTable.instantiate()
quadruple = Quad.instantiate()
jumps = Jumps.instantiate()
pointer = None

while True:
    try:
      reading = input('Name of file > ')
      correct = reading
      correctFile = open(correct, 'r')
      curr = correctFile.read()
      correctFile.close()
      if piser.parse(curr) == 'SUCCESS':
        print("SUCCESSFULLY COMPILED!")
      # symbolTable.printingAll()
      quadruple.print()
      symbolTable.reset()
      quadruple.reset()

    except EOFError:
      print("INCORRECT")
    if not reading: continue
