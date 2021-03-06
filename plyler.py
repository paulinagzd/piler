# Paulina Gonzalez Davalos
# Luis Felipe Miranda Icazbalceta
# A01194111
# A00820799
# Piler's Lexer and Parser in PLY

import ply.lex as lex
import ply.yacc as yacc
from symbolTable import SymbolTable
from semanticCube import SemanticCube
from quad import Quad
from jumps import Jumps
import quadHelpers
import condHelpers
import moduleHelpers
import helpers
import sys
sys.tracebacklimit=0 # depends on the amount of errors to log

# instantiating singleton classes
symbolTable = SymbolTable.instantiate()
quadruple = Quad.instantiate()
jumps = Jumps.instantiate()

# global variables for syntax checking
pointer = None
classPointer = None
funcPointer = None
aux = False
cont = 0
varArr = []
varDim = []

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
  'do' : 'DO',
  'class' : 'CLASS',
  'att' : 'ATTRIBUTES',
  'met' : 'METHODS',
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
  t.lineno += t.value.count('\n')

def t_CSTCHAR(t):
  r'\'[\w]\''
  t.value = str(t.value)
  return t

def t_CSTSTRING(t):
  r'("(\\"|[^"])*") | (\'(\\\'|[^\'])*\')' # escaping quotes
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

# GRAMMAR
################################################
# PROGRAM STRUCTURE
def p_program(p):
  '''
  program : PROGRAM ID SEMICOLON saw_program program_content main
  '''
  p[0] = 'SUCCESS'

def p_program_content(p):
  '''
  program_content : dec program_content
                  | class program_content
                  | function program_content
                  | empty
  '''

################################################
# FUNCTIONS
def p_main(p):
  '''
  main : INT MAIN saw_main OPAREN CPAREN block scope_end
  '''

def p_functions(p): # function declarations in a FIXED PLACE (such as class methods)
  '''
  functions : function functions
            | empty
  '''

def p_function(p):
  '''
  function : FUNCTION func1 ID saw_id saw_function OPAREN param CPAREN start_function_temp_count block end_function_temp_count saw_function_end scope_end
  '''

def p_function1(p):
  '''
  func1 : simple
        | VOID saw_type
  '''

def p_param(p):
  '''
  param : param2 param1
        | empty
  '''

def p_param1(p):
  '''
  param1 : COMMA param2 param1
         | empty
  '''

def p_param2(p): ####### OJO
  '''
  param2 : simple ID saw_id saw_variable_param
         | multiple ID saw_id OBRACKET CSTINT saw_end_value CBRACKET saw_dimension type3 saw_variable_param
  '''

################################################
# CLASSES
def p_class(p):
  '''
  class : CLASS ID saw_id saw_class COLON class_block class_scope_end SEMICOLON
  '''

def p_class_block(p):
  ''' 
  class_block :  OCURLY ATTRIBUTES COLON decs METHODS COLON functions CCURLY
  '''

################################################
# WHILE LOOP
def p_while_loop(p):
  '''
  while_loop : WHILE saw_while cond2 THEN block SEMICOLON saw_while_end
  '''

################################################
# DO WHILE LOOP
def p_do_while_loop(p):
  '''
  do_while_loop : DO saw_while block WHILE cond2 saw_do_while_end SEMICOLON
  '''

 ################################################
# VARIABLE DECLARATION
# Used only when declaring variables in a new scope (not an expression)
def p_decs(p):
  '''
  decs : dec decs1
  '''

def p_dec(p):
  '''
  dec : VAR type SEMICOLON
  '''

def p_decs1(p):
  '''
  decs1 : decs
        | empty
  '''

################################################
# TYPE
# Handles the conditions between the type being appropriate for its declaration
def p_type(p):
  '''
  type : simple ID saw_id saw_variable type1
       | multiple ID saw_id OBRACKET CSTINT saw_declared_dim CBRACKET type3 arr_dec saw_variable type2
  '''

def p_arr_dec(p):
  '''
  arr_dec : AS OCURLY arr_dec2 CCURLY
  '''

def p_arr_dec2(p):
  '''
  arr_dec2 : arr_dec_base arr_dec3
           | arrcst arr_dec4
  '''

def p_arr_dec3(p):
  '''
  arr_dec3 : COMMA arr_dec_base arr_dec3
           | empty
  '''

def p_arr_dec4(p):
  '''
  arr_dec4 : COMMA arrcst arr_dec4
           | empty
  '''

def p_arr_dec_base(p):
  '''
  arr_dec_base : OCURLY arrcst arr_dec4 CCURLY append_dim
  '''

def p_type1(p):
  '''
  type1 : COMMA ID saw_id saw_variable type1
        | empty
  '''

def p_type2(p):
  '''
  type2 : COMMA ID saw_id OBRACKET CSTINT saw_declared_dim CBRACKET type3 saw_variable
        | empty
  '''

def p_type3(p):
  '''
  type3 : OBRACKET CSTINT saw_declared_dim CBRACKET
        | empty
  '''

def p_type_simple(p):
  '''
  simple : INT saw_type
         | FLOAT saw_type
         | BOOL saw_type
         | STRING saw_type
         | CHAR saw_type
  '''

# arrays and matrices are declared with plural values
def p_type_multiple(p):
  '''
  multiple : INTS saw_type
           | FLOATS saw_type
           | BOOLS saw_type
           | STRINGS saw_type
           | CHARS saw_type
  '''

################################################
# BLOCK
def p_block(p):
  '''
  block : OCURLY b1 CCURLY
        | OCURLY decs count_vars b1 CCURLY
  '''

def p_b1(p):
  '''
  b1 : stmt b1
     | empty
  '''

################################################
# STATEMENT
def p_stmt(p):
  '''
  stmt : assign
       | function_call
       | conditional
       | write
       | read
       | while_loop
       | do_while_loop
       | ternary
       | RETURN saw_return_value exp
  '''

# FOR TERNARY AND ONE LINERS
def p_stmt_redux(p): 
  '''
  stmt_redux : assign
             | function_call
             | write
             | read
             | ternary
             | RETURN saw_return_value exp
  '''

################################################
# ASSIGNATION
def p_assign(p):
  '''
  assign : variable saw_var_factor AS saw_asig exp
  '''

################################################
# CONDITIONAL
def p_conditional(p):
  '''
  conditional : IF cond2 THEN block cond1 SEMICOLON bc_end
  '''

def p_cond1(p):
  '''
  cond1 : ELSE saw_else block
        | empty
  '''

def p_cond2(p):
  '''
    cond2 : OPAREN exp CPAREN
  '''

################################################
# TERNARY CONDITIONAL
def p_ternary(p):
  '''
  ternary : exp QUESTION saw_cond stmt_redux COLON saw_else stmt_redux SEMICOLON bc_end
  '''

################################################
# WRITE (PRINT)
def p_write(p):
  '''
  write : PRINT saw_print OPAREN exp e1 CPAREN saw_print_end
  '''

def p_e1(p):
  '''
  e1 : COMMA exp e1
     | empty
  '''

################################################
# READ (INPUT)
def p_read(p):
  '''
  read  : READ saw_read OPAREN variable saw_read_exp l1 CPAREN saw_read_end
  '''

def p_l1(p):
  '''
  l1 : COMMA variable saw_read_exp e1
     | empty
  '''
################################################
# BOOLEAN
def p_boolean(p):
  '''
  boolean : TRUE saw_end_value
          | FALSE saw_end_value
  '''

################################################
# VARIABLE (CALLING)
def p_variable(p):
  '''
  variable : ID saw_id saw_called_var
           | ID saw_id_arr OBRACKET is_dim exp CBRACKET variable1 end_dim saw_called_var
           | ID saw_id variable2
  '''

def p_variable1(p):
  '''
  variable1 : OBRACKET is_second_dim exp CBRACKET
            | empty
  '''

def p_variable2(p):
  '''
  variable2 : PERIOD ID saw_called_var_from_class
            | PERIOD ID saw_called_var_from_class saw_id_arr_class OBRACKET is_dim exp CBRACKET variable1 end_dim
  '''

################################################
# FUNCTION (CALLING)
def p_function_call(p):
  '''
  function_call : ID saw_id verify_func OPAREN exp verify_param function_call1 CPAREN generate_gosub
                | ID saw_id verify_func OPAREN CPAREN generate_gosub
                | ID saw_id function_call2
  '''

def p_function_call1(p):
  '''
  function_call1 : COMMA increment_cont exp verify_param function_call1
                 | empty
  '''

def p_function_call2(p):
  '''
  function_call2 : PERIOD ID saw_called_func_from_class verify_func OPAREN exp verify_param function_call1 CPAREN generate_gosub_obj
                 | PERIOD ID saw_called_func_from_class verify_func OPAREN CPAREN generate_gosub_obj
  '''

################################################
# SUPER EXP
def p_exp(p):
  '''
  exp : texp exp1 check_or_operator
  '''
  quadHelpers.expression_evaluation(p)

def p_exp1(p):
  '''
  exp1 : OR saw_or texp exp1
       | empty
  '''

def p_texp(p):
  '''
  texp : gexp texp1 check_and_operator
  '''

def p_texp1(p):
  '''
  texp1 : AND saw_and gexp texp1
        | empty
  '''

def p_gexp(p):
  '''
  gexp : mexp gexp1 check_relational_operator
  '''

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

def p_mexp(p):
  '''
  mexp : term mexp1
  '''

def p_mexp1(p):
  '''
  mexp1 : PLUS saw_plusminus_operator term mexp1
        | MINUS saw_plusminus_operator term mexp1
        | empty
  '''

################################################
# TERM
def p_term(p):
  '''
  term : factor term1 check_plusminus_operator
  '''

def p_term1(p):
  '''
  term1 : MULT saw_multdiv_operator factor term1
        | DIV saw_multdiv_operator factor term1
        | empty
  '''

################################################
# FACTOR
def p_factor(p):
  '''
  factor : OPAREN saw_oparen exp CPAREN saw_cparen check_multdiv_operator
         | varcst check_multdiv_operator
         | variable saw_var_factor check_multdiv_operator
         | OCURLY saw_oparen function_call CCURLY saw_cparen check_multdiv_operator
  '''

def p_saw_var_factor(p):
  '''
  saw_var_factor :
  '''
  global aux
  global classPointer
  if aux:
    quadruple.pilaArr.pop()
    aux = False
    pass
  elif classPointer != None and classPointer.getIsObject():
    quadruple.pilaO.append(classPointer.getVirtualAddress())
  else:
    current = symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName())
    quadruple.pilaO.append(current.getVirtualAddress())
  classPointer = None

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : CSTINT saw_end_value
         | CSTFLT saw_end_value
         | CSTCHAR saw_end_value
         | CSTSTRING saw_end_value
         | boolean
  '''

def p_arrcst(p):
  '''
  arrcst : CSTINT append_val
         | CSTFLT append_val
         | CSTCHAR append_val
         | CSTSTRING append_val
  '''

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
def p_saw_program(p):
  ''' saw_program : '''
  condHelpers.saveForMain()

def p_saw_main(p):
  ''' saw_main : '''
  condHelpers.enterMain()

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

def p_saw_id_arr(p):
  ''' saw_id_arr : '''
  current = symbolTable.getCurrentScope()
  current.setLatestName(p[-1])
  global pointer
  pointer = current.sawCalledVariable(current.getLatestName())
  quadruple.pilaO.append(pointer.getVirtualAddress())
  quadruple.pilaArr.append(pointer)

def p_saw_id_arr_class(p):
  ''' saw_id_arr_class : '''
  current = symbolTable.getCurrentScope()
  aux = current.getLatestName()
  symbolTable.getCurrentScope().setLatestName(p[-1])
  global pointer
  pointer = current.doesClassExist(aux)
  quadruple.pilaO.append(pointer.getVirtualAddress())
  quadruple.pilaArr.append(pointer)

def p_saw_variable(p):
  ''' saw_variable : '''
  global varDim
  global varArr
  current = symbolTable.getCurrentScope()
  isParam = False
  if len(varArr) > 0:
    varDim.append(varArr)
  varArr = []
  dimensions = current.getLatestDimension()
  current.addVariable(current.getLatestName(), current.getLatestType(), dimensions, isParam, varDim)
  varDim = []

def p_saw_variable_param(p):
  ''' saw_variable_param : '''
  current = symbolTable.getCurrentScope()
  isParam = True
  current.addVariable(current.getLatestName(), current.getLatestType(), current.getLatestDimension(), isParam, None)

def p_saw_dimension(p):
  ''' saw_dimension : '''

def p_saw_called_var(p):
  ''' saw_called_var : '''
  current = symbolTable.getCurrentScope()
  global pointer
  pointer = current.sawCalledVariable(current.getLatestName())

def p_saw_called_var_from_class(p):
  ''' saw_called_var_from_class : '''
  global classPointer
  current = symbolTable.getCurrentScope()
  temp = current.getLatestName()
  current.setLatestName(p[-1])
  classPointer = current.doesClassExist(temp, p[-1], 'var')

def p_saw_called_func_from_class(p):
  ''' saw_called_func_from_class : '''
  global funcPointer
  current = symbolTable.getCurrentScope()
  temp = current.getLatestName()
  current.setLatestName(p[-1])
  funcPointer = current.doesClassExist(temp, p[-1], 'func')

def p_saw_asig(p):
  ''' saw_asig : '''
  quadruple.pOper.append(p[-1])

def p_saw_end_value(p):
  ''' saw_end_value : '''
  constType = helpers.getTypeConstants(p[-1])
  symbolTable.getCurrentScope().addConstant(p[-1], constType)
  tempAddressPointer = symbolTable.getGlobalScope().getScopeConstants()[constType]
  curr = p[-1]
  tempAddress = tempAddressPointer[curr]
  # print("EXP", curr, tempAddress)
  quadruple.pilaO.append(tempAddress)

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
  res = quadHelpers.check_and_or_operator(quadruple)

def p_check_or_operator(p):
  '''
  check_or_operator :
  '''
  workingStack = quadruple.getWorkingStack()
  res = quadHelpers.check_and_or_operator(quadruple)

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

def p_saw_function_end(p):
  ''' saw_function_end : '''
  quadruple.saveQuad('endfunc', -1, -1, -1)
  quadHelpers.tempCounter = 0


def p_scope_end(p):
  ''' scope_end : '''
  if symbolTable.getCurrentScope().getContext() == "global":
    quadruple.saveQuad("end", -1, -1, -1)
  else:
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
    quadruple.saveQuad('read', -1, -1, read_operand.getVirtualAddress())

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

def p_saw_do_while_end(p):
  ''' saw_do_while_end : '''
  condHelpers.exitDoWhile()

def p_count_vars(p):
  ''' count_vars : '''
  symbolTable.getCurrentScope().countVars()

def p_verify_func(p):
  ''' verify_func : '''
  global funcPointer
  extraParam = ''
  keyword = ''
  if funcPointer != None:
    keyword = 'class'
    extraParam = funcPointer
  else:
    keyword = 'global'
    extraParam = ''
  symbolTable.getCurrentScope().sawCalledFunction(symbolTable.getCurrentScope().getLatestName(), keyword, extraParam)

def p_verify_param(p):
  ''' verify_param : '''
  global cont
  cont = moduleHelpers.verifyParamMatch(cont)


def p_increment_cont(p):
  ''' increment_cont : '''
  global cont
  cont = moduleHelpers.incrementParamCounter(cont)

def p_generate_gosub(p):
  ''' generate_gosub : '''
  moduleHelpers.generateGoSub(False, '')
  global cont
  cont = 0

def p_generate_gosub_obj(p):
  ''' generate_gosub_obj : '''
  global funcPointer
  moduleHelpers.generateGoSub(True, funcPointer)
  global cont
  cont = 0

def p_saw_cond(p):
  ''' saw_cond : '''
  condHelpers.enterCond()

def p_saw_declared_dim(p):
  ''' saw_declared_dim : '''
  current = symbolTable.getCurrentScope()
  current.setLatestDimension(p[-1])
  constType = helpers.getTypeConstants(p[-1])
  symbolTable.getCurrentScope().addConstant(p[-1], constType)
  tempAddressPointer = symbolTable.getGlobalScope().getScopeConstants()[constType]

def p_is_dim(p):
  ''' is_dim : '''
  current = symbolTable.getCurrentScope()
  global pointer
  pointer = current.sawCalledVariable(current.getLatestName())
  if pointer.getDimensions() > 0:
    dim = 1
    quadruple.pilaDim.append({"id": pointer, "dim": dim})
    quadruple.pOper.append('$') #fake bottom 

def p_is_second_dim(p):
  ''' is_second_dim : '''
  for i in quadruple.pilaDim:
    if i["id"] == quadruple.pilaArr[-1]:
      i["dim"] = 2

def p_end_dim(p):
  ''' end_dim : '''
  global aux
  aux = quadHelpers.endDim(quadruple.pilaArr[-1])

def p_saw_return_value(p):
  ''' saw_return_value : '''
  quadruple.pOper.append(p[-1])

def p_start_function_temp_count(p):
  '''
  start_function_temp_count : 
  '''
  
def p_append_val(p):
  '''
  append_val : 
  '''
  global varArr
  varArr.append(p[-1])

def p_append_dim(p):
  '''
  append_dim : 
  '''
  global varDim
  global varArr
  varDim.append(varArr)
  varArr = []

def p_end_function_temp_count(p):
  '''
  end_function_temp_count : 
  '''
def resetGlobals():
  global pointer
  global classPointer
  global funcPointer
  global aux
  global cont

  pointer = None
  classPointer = None
  funcPointer = None
  aux = False
  cont = 0

parser = yacc.yacc()
