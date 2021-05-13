import ply.lex as lex
import ply.yacc as yacc
import quadHelpers
import condHelpers
from symbolTable import SymbolTable
from semanticCube import SemanticCube
from quad import Quad
from jumps import Jumps

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

# grammar
################################################

# PROGRAMA
def p_programa(p):
  '''
  programa : PROGRAM ID SEMICOLON bloque
           | PROGRAM ID SEMICOLON dec bloque
  '''

################################################
# FUNCION
def p_funcion(p):
  '''
  funcion : FUNCTION func1 ID saw_id saw_function OPAREN param CPAREN bloque
  '''

def p_funcion1(p):
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

def p_param2(p):
  '''
  param2 : simple ID saw_id saw_variable_param
         | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable_param
  '''

################################################
# CLASE
def p_clase(p):
  '''
    clase : CLASS ID saw_id saw_class COLON clase_bloque SEMICOLON
  '''

def p_clase_bloque(p):
  ''' 
  clase_bloque :  OCURLY ATTRIBUTES COLON clase_bloque1 METHODS COLON clase_metodos_bloque class_scope_end CCURLY
  '''

def p_clase_bloque1(p):
  ''' 
  clase_bloque1 : dec
                | empty
  '''  

def p_clase_metodos_bloque(p):
  ''' 
  clase_metodos_bloque : funcion clase_metodos_bloque
                       | empty
  '''

################################################
# CICLO WHILE
def p_ciclo_while(p):
  '''
  ciclo_while : WHILE saw_while cond2 THEN bloque_ciclo SEMICOLON saw_while_end
  '''

################################################
# CICLO FOR
def p_ciclo_for(p):
  '''
  ciclo_for : FOR OPAREN variable FROM ciclo_for1 TO ciclo_for1 BY ciclo_for1 CPAREN THEN bloque_ciclo SEMICOLON
  '''

def p_ciclo_for1(p):
  '''
  ciclo_for1 : CSTINT
             | variable
  '''

 ################################################
# DECLARACION VARS
def p_dec(p):
  '''
  dec : VAR tipo SEMICOLON dec1
  '''

def p_dec1(p):
  '''
  dec1 : dec
       | empty
  '''

################################################
# TIPO
def p_tipo(p):
  '''
  tipo : compuesto ID saw_id saw_variable tipo1
       | simple ID saw_id saw_variable tipo1
       | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable tipo2
  '''

def p_tipo1(p):
  '''
  tipo1 : COMMA ID saw_id saw_variable tipo1
        | empty
  '''

def p_tipo2(p):
  '''
  tipo2 : COMMA ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable
        | empty
  '''

def p_tipo3(p):
  '''
  tipo3 : OBRACKET CSTINT CBRACKET saw_dimension
        | empty
  '''

def p_tipo_simple(p):
  '''
  simple : INT saw_type
         | FLOAT saw_type
         | BOOL saw_type
         | STRING saw_type
         | CHAR saw_type
  '''

def p_tipo_multiple(p):
  '''
  multiple : INTS saw_type
           | FLOATS saw_type
           | BOOLS saw_type
           | STRINGS saw_type
           | CHARS saw_type
  '''

def p_tipo_compuesto(p):
  '''
  compuesto : ID saw_type
            | DATAFRAME saw_type
            | FILE saw_type
  ''' 

################################################
# BLOQUE
def p_bloque(p):
  '''
  bloque : OCURLY b1 CCURLY scope_end
  '''

def p_b1(p):
  '''
  b1 : estatuto b1
     | empty
  '''

# BLOQUE CICLO
def p_bloque_ciclo(p):
  '''
  bloque_ciclo : OCURLY bc1 CCURLY
  '''

def p_bc1(p):
  '''
  bc1 : estatuto_ciclo bc1
      | empty
  '''

################################################
# ESTATUTO
def p_estatuto(p):
  '''
  estatuto : asignacion
           | llamada
           | condicion
           | escritura
           | leer
           | ciclo_while
           | ciclo_for
           | ternaria
           | bloque
           | funcion
           | clase
           | dec
  '''

def p_estatuto_ciclo(p):
  '''
  estatuto_ciclo : asignacion
                 | condicion
                 | escritura
                 | leer
                 | ciclo_while
                 | ciclo_for
                 | dec
  '''

def p_estatuto_redux(p):
  '''
  estatuto_redux : asignacion
                 | llamada
                 | escritura
                 | leer
                 | ternaria
  '''

################################################
# ASIGNACION
def p_asignacion(p):
  '''
  asignacion : variable saw_var_factor AS saw_asig exp
  '''

################################################
# CONDICIONAL
def p_condicion(p):
  '''
  condicion : IF cond2 THEN bloque_ciclo cond1 SEMICOLON bc_end
  '''

def p_cond1(p):
  '''
  cond1 : ELSE saw_else bloque_ciclo
        | empty
  '''

def p_cond2(p):
  '''
    cond2 : OPAREN exp CPAREN
  '''

################################################
# condicion ternaria
def p_ternaria(p):
  '''
  ternaria : exp QUESTION estatuto_redux COLON estatuto_redux SEMICOLON
  '''

################################################
# ESCRITURA
def p_escritura(p):
  '''
  escritura : PRINT saw_print OPAREN exp e1 CPAREN saw_print_end
  '''

def p_e1(p):
  '''
  e1 : COMMA exp e1
     | empty
  '''

################################################
# LECTURA
def p_leer(p):
  '''
  leer  : READ saw_read OPAREN variable saw_read_exp l1 CPAREN saw_read_end
  '''

def p_l1(p):
  '''
  l1 : COMMA variable saw_read_exp e1
     | empty
  '''

################################################
# BOOLEANOS
def p_boolean(p):
  '''
  boolean : TRUE
          | FALSE
  '''

################################################
# LLAMADA DE VARIABLES
def p_variable(p):
  '''
  variable : ID saw_id saw_called_var
           | ID saw_id OBRACKET exp CBRACKET saw_dimension variable1 saw_called_var
           | ID saw_id variable2
  '''

def p_variable1(p):
  '''
  variable1 : OBRACKET exp CBRACKET saw_dimension
            | empty
  '''

def p_variable2(p):
  '''
  variable2 : PERIOD ID saw_called_var_from_class
            | PERIOD ID saw_called_var_from_class OBRACKET exp CBRACKET saw_dimension variable1
  '''

################################################
# LLAMADA DE FUNCION
def p_llamada_funcion(p):
  '''
  llamada : ID saw_id OPAREN exp llamada1 CPAREN
          | ID saw_id OPAREN CPAREN
  '''

def p_llamada_funcion1(p):
  '''
  llamada1 : COMMA exp llamada1
           | empty
  '''

################################################
# MANEJO DE EXPRESIONES
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
  mexp : termino mexp1
  '''

def p_mexp1(p):
  '''
  mexp1 : PLUS saw_plusminus_operator termino mexp1
        | MINUS saw_plusminus_operator termino mexp1
        | empty
  '''

################################################
# TERMINO
def p_termino(p):
  '''
  termino : factor term1 check_plusminus_operator
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
         | llamada
  '''

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

pilex = lex.lex()
piser = yacc.yacc()