# Paulina Gonzalez Davalos
# Luis Felipe Miranda Icazbalceta
# A01194111
# A00820799
# Lexer y Parser de Piler en PLY

import ply.lex as lex
import ply.yacc as yacc
from symbolTable import SymbolTable
from semanticCube import SemanticCube
from quad import Quad
from jumps import Jumps
import quadHelpers
import condHelpers
import sys
# sys.tracebacklimit=0

symbolTable = SymbolTable.instantiate()
quadruple = Quad.instantiate()
jumps = Jumps.instantiate()

pointer = None

# reserved words
reserved = {
  'program' : 'PROGRAM',
  'func' : 'FUNCTION',
  'void' : 'VOID',
  'print' : 'PRINT',
  'read' : 'READ',
  'var' : 'VAR',
  'int' : 'INT',
  'flt' : 'FLOAT',
  'cha' : 'CHAR', 
  'str' : 'STRING',
  'boo' : 'BOOL',
  'True' : 'TRUE',
  'False' : 'FALSE',
  'ints': 'INTS',
  'flts': 'FLOATS',
  'strs': 'STRINGS',
  'chas' : 'CHARS',
  'boos' : 'BOOLS',
  'if' : 'IF',
  'then' : 'THEN',
  'else' : 'ELSE',
  'while' : 'WHILE',
  'for' : 'FOR',
  'from' : 'FROM',
  'to' : 'TO',
  'by' : 'BY',
  'class' : 'CLASS',
  'att' : 'ATTRIBUTES',
  'met' : 'METHODS',
  'file' : 'FILE',
  'dataframe' : 'DATAFRAME',
  'return' : 'RETURN',
  'main' : 'MAIN',
}

# terminals and regEx
tokens = [
  'CSTINT',
  'CSTFLT',
  'CSTSTRING',
  'CSTCHAR',
  'ID',
  'COMMENT',
  'PLUS',
  'MINUS',
  'MULT',
  'DIV',
  'OPAREN',
  'CPAREN',
  'OCURLY',
  'CCURLY',
  'OBRACKET',
  'CBRACKET',
  'PERIOD',
  'COMMA',
  'COLON',
  'SEMICOLON',
  'QUESTION',
  'AND',
  'OR',
  'AS',
  'GT',
  'LT',
  'NE',
  'EQ',
  'GTE',
  'LTE',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_OCURLY = r'\{'
t_CCURLY = r'\}'
t_OBRACKET = r'\['
t_CBRACKET = r'\]'
t_PERIOD = r'\.'
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_QUESTION = r'\?'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_AS = r'\='
t_GT = r'\>'
t_LT = r'\<'
t_NE = r'\!\='
t_EQ = r'\=\='
t_GTE = r'\>\='
t_LTE = r'\<\='

t_ignore = r' '

def t_CSTFLT(t):
  r'-?\d+\.\d+'
  t.value = float(t.value)
  return t

def t_CSTINT(t):
  r'-?\d+'
  t.value = int(t.value)
  return t

def t_ID(t):
  r'[A-Za-z]([A-Za-z]|[0-9])*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_COMMENT(t):
  r'(?s)/\*.*?\*/'
  # r'/\*(.|\n)*?\*/'
  t.lineno += t.value.count('\n')

def t_CSTCHAR(t):
  r'\'[\w]\''
  t.value = str(t.value)
  return t

def t_CSTSTRING(t):
  r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')' # escaping quotes
  t.value = str(t.value)
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


def t_error(t):
  print("ERROR! at")
  print(t)
  t.lexer.skip(1)

lexer = lex.lex()

# grammar
################################################

# program
def p_program(p):
  '''
  program : PROGRAM ID SEMICOLON program_content main
  '''
  p[0] = tuple(p[1:])

def p_program_content(p):
  '''
  program_content : dec program_content
                  | class program_content
                  | function program_content
                  | empty
  '''
  p[0] = tuple(p[1:])

################################################
# function
def p_main(p):
  '''
  main : INT MAIN saw_main OPAREN CPAREN block scope_end
  '''
  p[0] = tuple(p[1:])

def p_functions(p): # function declarations in a FIXED PLACE (such as class methods)
  '''
  functions : function functions
            | empty
  '''

def p_function(p):
  '''
  function : FUNCTION func1 ID saw_id saw_function OPAREN param CPAREN block scope_end
  '''
  p[0] = tuple(p[1:])

def p_function1(p):
  '''
  func1 : simple
        | VOID saw_type
  '''
  p[0] = p[1]


def p_param(p):
  '''
  param : param2 param1
        | empty
  '''
  p[0] = tuple(p[1:])


def p_param1(p):
  '''
  param1 : COMMA param2 param1
         | empty
  '''
  p[0] = tuple(p[1:])

def p_param2(p): ####### OJO
  '''
  param2 : simple ID saw_id saw_variable_param
         | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension type3 saw_variable_param
  '''
  p[0] = tuple(p[1:])

################################################
# class
def p_class(p):
  '''
  class : CLASS ID saw_id saw_class COLON class_block class_scope_end SEMICOLON
  '''
  p[0] = tuple(p[1:])

def p_class_block(p):
  ''' 
  class_block :  OCURLY ATTRIBUTES COLON decs METHODS COLON functions CCURLY
  '''
  p[0] = tuple(p[1:])

################################################
# CICLO WHILE
def p_while_loop(p):
  '''
  while_loop : WHILE saw_while cond2 THEN block SEMICOLON saw_while_end
  '''
  p[0] = tuple(p[1:])

################################################
# CICLO FOR
def p_for_loop(p):
  '''
  for_loop : FOR OPAREN variable FROM for_loop1 TO for_loop1 BY for_loop1 CPAREN THEN block SEMICOLON
  '''
  p[0] = tuple(p[1:])


def p_for_loop1(p):
  '''
  for_loop1 : CSTINT
            | variable
  '''
  p[0] = tuple(p[1:])

 ################################################
# DECLARACION VARS
def p_decs(p):
  '''
  decs : dec decs1
  '''
  p[0] = tuple(p[1:])

def p_dec(p):
  '''
  dec : VAR type SEMICOLON dec1
  '''
  p[0] = tuple(p[1:])

def p_dec1(p):
  '''
  dec1 : dec
       | empty
  '''
  p[0] = p[1]

def p_decs1(p):
  '''
  decs1 : decs
        | empty
  '''
  p[0] = p[1]
################################################
# type
def p_type(p):
  '''
  type : compound ID saw_id saw_variable type1
       | simple ID saw_id saw_variable type1
       | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension type3 saw_variable type2
  '''
  p[0] = tuple(p[1:])

def p_type1(p):
  '''
  type1 : COMMA ID saw_id saw_variable type1
        | empty
  '''
  p[0] = tuple(p[1:])

def p_type2(p):
  '''
  type2 : COMMA ID saw_id OBRACKET CSTINT CBRACKET saw_dimension type3 saw_variable
        | empty
  '''
  p[0] = tuple(p[1:])

def p_type3(p):
  '''
  type3 : OBRACKET CSTINT CBRACKET saw_dimension
        | empty
  '''
  p[0] = tuple(p[1:])

def p_type_simple(p):
  '''
  simple : INT saw_type
         | FLOAT saw_type
         | BOOL saw_type
         | STRING saw_type
         | CHAR saw_type
  '''
  p[0] = p[1]

def p_type_multiple(p):
  '''
  multiple : INTS saw_type
           | FLOATS saw_type
           | BOOLS saw_type
           | STRINGS saw_type
           | CHARS saw_type
  '''
  p[0] = p[1]

def p_type_compound(p):
  '''
  compound : ID saw_type
            | DATAFRAME saw_type
            | FILE saw_type
  ''' 
  p[0] = p[1]

################################################
# block
def p_block(p):
  '''
  block : OCURLY b1 CCURLY
        | OCURLY decs count_vars b1 CCURLY
  '''
  p[0] = tuple(p[1:])

def p_b1(p):
  '''
  b1 : estatuto b1
     | empty
  '''
  p[0] = tuple(p[1:])

################################################
# ESTATUTO
def p_estatuto(p):
  '''
  estatuto : assign
           | llamada
           | conditional
           | write
           | read
           | while_loop
           | for_loop
           | ternary
           | RETURN exp
  '''
  p[0] = p[1]

def p_estatuto_redux(p): # TERNARY ONE LINERS
  '''
  estatuto_redux : assign
                 | llamada
                 | write
                 | read
                 | ternary
                 | RETURN exp
  '''
  p[0] = tuple(p[1:])

################################################
# assign
def p_assign(p):
  '''
  assign : variable saw_var_factor AS saw_asig exp
  '''
  p[0] = tuple(p[1:])

################################################
# conditional
def p_conditional(p):
  '''
  conditional : IF cond2 THEN block cond1 SEMICOLON bc_end
  '''
  p[0] = tuple(p[1:])

def p_cond1(p):
  '''
  cond1 : ELSE saw_else block
        | empty
  '''
  p[0] = tuple(p[1:])

def p_cond2(p):
  '''
    cond2 : OPAREN exp CPAREN
  '''
  p[0] = tuple(p[1:])

################################################
# conditional ternary
def p_ternary(p):
  '''
  ternary : exp QUESTION estatuto_redux COLON estatuto_redux SEMICOLON
  '''
  p[0] = tuple(p[1:])

################################################
# write
def p_write(p):
  '''
  write : PRINT saw_print OPAREN exp e1 CPAREN saw_print_end
  '''
  p[0] = tuple(p[1:])

def p_e1(p):
  '''
  e1 : COMMA exp e1
     | empty
  '''
  p[0] = tuple(p[1:])

################################################
# read
def p_read(p):
  '''
  read  : READ saw_read OPAREN variable saw_read_exp l1 CPAREN saw_read_end
  '''
  p[0] = tuple(p[1:])

def p_l1(p):
  '''
  l1 : COMMA variable saw_read_exp e1
     | empty
  '''
  p[0] = tuple(p[1:])
################################################
# BOOLEAN
def p_boolean(p):
  '''
  boolean : TRUE
          | FALSE
  '''
  p[0] = p[1]

################################################
# VARIABLE (llamada)
def p_variable(p):
  '''
  variable : ID saw_id saw_called_var
           | ID saw_id OBRACKET exp CBRACKET saw_dimension variable1 saw_called_var
           | ID saw_id variable2
  '''
  p[0] = tuple(p[1:])

def p_variable1(p):
  '''
  variable1 : OBRACKET exp CBRACKET saw_dimension
            | empty
  '''
  p[0] = tuple(p[1:])

def p_variable2(p):
  '''
  variable2 : PERIOD ID saw_called_var_from_class
            | PERIOD ID saw_called_var_from_class OBRACKET exp CBRACKET saw_dimension variable1
  '''
  p[0] = tuple(p[1:])

################################################
# LLAMADA function
def p_llamada_function(p):
  '''
  llamada : ID saw_id OPAREN exp llamada1 CPAREN
          | ID saw_id OPAREN CPAREN
  '''
  p[0] = tuple(p[1:])

def p_llamada_function1(p):
  '''
  llamada1 : COMMA exp llamada1
           | empty
  '''
  p[0] = tuple(p[1:])

################################################
# SUPER EXP
def p_exp(p):
  '''
  exp : texp exp1 check_or_operator
  '''
  if not quadruple.pOper or quadruple.pOper[-1] == '=' or quadruple.pOper[-1] == 'print':
    if not quadruple.pOper:
      if p[-2] == 'if' or p[-3] == 'while':
        condHelpers.enterCond()
      else:
        p[0] = quadruple.pilaO.pop()
        print('EVALUACION EXPRESION:', p[0])
      # symbolTable.getCurrentScope().setLatestExpValue(p[0])
    elif quadruple.pOper[-1] == '=':
      right_operand = quadruple.pilaO.pop() # this should be a value
      left_operand = quadruple.pilaO.pop() # this should be an id
      right_type = quadHelpers.getType(right_operand)
      left_var = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
      left_type = left_var.getVarType()      
      if right_type == left_type:
        quadruple.saveQuad('=', right_operand, None ,left_operand)
      quadruple.pOper.pop()
    elif quadruple.pOper[-1] == 'print':
      print_operand = quadruple.pilaO.pop() # this should be the value to print
      quadruple.saveQuad('print', None, None, print_operand)

def p_exp1(p):
  '''
  exp1 : OR saw_or texp exp1
       | empty
  '''
  p[0] = tuple(p[1:])

def p_texp(p):
  '''
  texp : gexp texp1 check_and_operator
  '''
  p[0] = tuple(p[1:])

def p_texp1(p):
  '''
  texp1 : AND saw_and gexp texp1
        | empty
  '''
  p[0] = tuple(p[1:])

def p_gexp(p):
  '''
  gexp : mexp gexp1 check_relational_operator
  '''
  p[0] = tuple(p[1:])

def p_gexp1(p):
  '''
  gexp1 : LT saw_relational_operator mexp
        | GT saw_relational_operator mexp
        | GTE saw_relational_operator mexp
        | LTE saw_relational_operator mexp
        | EQ saw_relational_operator mexp
        | NE saw_relational_operator mexp
        | empty
  '''
  p[0] = tuple(p[1:])

def p_mexp(p):
  '''
  mexp : termino mexp1
  '''

def p_mexp1(p):
  '''
  mexp1 : PLUS saw_plusminus_operator termino mexp1
        | MINUS saw_plusminus_operator termino mexp1
        | empty
  '''
  p[0] = tuple(p[1:])

################################################
# TERMINO
def p_termino(p):
  '''
  termino : factor term1 check_plusminus_operator
  '''
  p[0] = tuple(p[1:])

def p_term1(p):
  '''
  term1 : MULT saw_multdiv_operator factor term1
        | DIV saw_multdiv_operator factor term1
        | empty
  '''
  p[0] = tuple(p[1:])

################################################
# FACTOR
def p_factor(p):
  '''
  factor : OPAREN saw_oparen exp CPAREN saw_cparen check_multdiv_operator
         | varcst check_multdiv_operator
         | variable saw_var_factor check_multdiv_operator
         | llamada
  '''
  p[0] = tuple(p[1:])

def p_saw_var_factor(p):
  '''
  saw_var_factor :
  '''
  current = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
  # print(current)
  quadruple.pilaO.append(current)

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : CSTINT saw_end_value
         | CSTFLT saw_end_value
         | CSTCHAR saw_end_value
         | CSTSTRING saw_end_value
         | boolean saw_end_value
  '''
  p[0] = tuple(p[1:])

################################################
# EMPTY
def p_empty(p):
  '''
  empty : 
  '''
  p[0] = None

################################################
# ERROR
def p_error(p):
    raise Exception("SYNTAX ERROR! BEFORE THE {} ON LINE {}".format(p.value, p.lineno))
  
################################################
# AUX RULES FOR SYMBOL TABLE
def p_saw_main(p):
  ''' saw_main : '''
  p[0] = tuple(p[1:])

def p_saw_class(p):
  ''' saw_class : '''
  symbolTable.getCurrentScope().setLatestName(p[-2])
  symbolTable.getCurrentScope().addClass(symbolTable.getCurrentScope().getLatestName())

def p_saw_type(p):
  ''' saw_type : '''
  symbolTable.getCurrentScope().setLatestType(p[-1])

def p_saw_id(p):
  ''' saw_id : '''
  symbolTable.getCurrentScope().setLatestName(p[-1])

def p_saw_variable(p):
  ''' saw_variable : '''
  current = symbolTable.getCurrentScope()
  isParam = False
  current.addVariable(current.getLatestName(), current.getLatestType(), current.getLatestDimension(), isParam)

def p_saw_variable_param(p):
  ''' saw_variable_param : '''
  current = symbolTable.getCurrentScope()
  isParam = True
  current.addVariable(current.getLatestName(), current.getLatestType(), current.getLatestDimension(), isParam)

def p_saw_dimension(p):
  ''' saw_dimension : '''
  current = symbolTable.getCurrentScope()
  current.setLatestDimension()

def p_saw_called_var(p):
  ''' saw_called_var : '''
  current = symbolTable.getCurrentScope()
  global pointer
  pointer = current.sawCalledVariable(current.getLatestName())

def p_saw_called_var_from_class(p):
  ''' saw_called_var_from_class : '''
  current = symbolTable.getCurrentScope()
  temp = current.getLatestName()
  current.setLatestName(p[-1])
  current.doesClassExist(temp, p[-1])

def p_saw_asig(p):
  ''' saw_asig : '''
  quadruple.pOper.append(p[-1])

def p_saw_end_value(p):
  ''' saw_end_value : '''
  quadruple.pilaO.append(p[-1])

def p_saw_plusminus_operator(p):
  ''' saw_plusminus_operator  : '''
  quadruple.pOper.append(p[-1])

def p_check_plusminus_operator(p):
  ''' check_plusminus_operator  : '''
  res = quadHelpers.check_plusminus_operator(quadruple)

def p_saw_multdiv_operator(p):
  ''' saw_multdiv_operator  : '''
  quadruple.pOper.append(p[-1])

def p_check_multdiv_operator(p):
  ''' check_multdiv_operator  : '''
  quadHelpers.check_multdiv_operator(quadruple)

def p_saw_relational_operator(p):
  ''' saw_relational_operator : '''
  quadruple.pOper.append(p[-1])

def p_check_relational_operator(p):
  ''' check_relational_operator : '''
  workingStack = quadruple.getWorkingStack()
  quadHelpers.check_relational_operator(quadruple)

def p_check_and_operator(p):
  '''
  check_and_operator  :
  '''
  workingStack = quadruple.getWorkingStack()
  res = quadHelpers.check_and_operator(quadruple)

def p_check_or_operator(p):
  '''
  check_or_operator :
  '''
  workingStack = quadruple.getWorkingStack()
  res = quadHelpers.check_or_operator(quadruple)

def p_saw_and(p):
  '''
  saw_and  :
  '''
  quadruple.pOper.append(p[-1])

def p_saw_or(p):
  '''
  saw_or :
  '''
  quadruple.pOper.append(p[-1])

def p_saw_oparen(p):
  ''' saw_oparen : '''
  quadruple.pOper.append(p[-1])

def p_saw_cparen(p):
  ''' saw_cparen : '''
  if quadruple.pOper:
    quadruple.pOper.pop()

def p_saw_function(p):
  ''' saw_function : '''
  current = symbolTable.getCurrentScope()
  current.addFunction(symbolTable.getCurrentScope().getLatestName(), symbolTable.getCurrentScope().getLatestType())

def p_scope_end(p):
  ''' scope_end : '''
  symbolTable.exitScope()

def p_class_scope_end(p):
  ''' class_scope_end : '''
  symbolTable.exitClassScope()

def p_saw_print(p):
  ''' saw_print : '''
  quadruple.pOper.append(p[-1])

def p_saw_print_end(p):
  ''' saw_print_end : '''
  quadruple.pOper.pop()

def p_saw_read(p):
  ''' saw_read : '''
  quadruple.pOper.append(p[-1])

def p_saw_read_exp(p):
  ''' saw_read_exp : '''
  if quadruple.pOper[-1] == 'read':
    current = symbolTable.getCurrentScope()
    read_operand = current.sawCalledVariable(current.getLatestName())
    quadruple.saveQuad('read', None, None, read_operand)

def p_saw_read_end(p):
  ''' saw_read_end : '''
  quadruple.pOper.pop()

def p_bc_end(p):
  ''' bc_end : '''
  condHelpers.exitIf()

def p_saw_else(p):
  '''saw_else : '''
  condHelpers.enterElse()

def p_saw_while(p):
  '''saw_while : '''
  jumps.setStackPush(quadruple.quadCounter)

def p_saw_while_end(p):
  ''' saw_while_end : '''
  condHelpers.exitWhile()

def p_count_vars(p):
  ''' count_vars : '''
  symbolTable.getCurrentScope().countVars()

parser = yacc.yacc()

# lexer.input(
#   '''
#   '''
# )

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
      # symbolTable.printingAll()
      quadruple.print()
      symbolTable.reset()
      quadruple.reset()

    except EOFError:
      print("INCORRECT")
    if not reading: continue
