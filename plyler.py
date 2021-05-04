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
import quadHelpers
import sys

symbolTable = SymbolTable.instantiate()
quadruple = Quad.instantiate()

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

lexer = lex.lex()

# grammar
################################################

# PROGRAMA
def p_programa(p):
  '''
  programa : PROGRAM ID saw_program SEMICOLON bloque
           | PROGRAM ID saw_program SEMICOLON dec bloque
  '''
  p[0] = tuple(p[1:])

################################################
# FUNCION
def p_funcion(p):
  '''
  funcion : FUNCTION func1 ID saw_id saw_function OPAREN param CPAREN bloque
  '''
  p[0] = tuple(p[1:])


def p_funcion1(p):
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
         | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable_param
  '''
  p[0] = tuple(p[1:])

################################################
# CLASE
def p_clase(p):
  '''
    clase : CLASS ID saw_id saw_class COLON clase_bloque SEMICOLON
  '''
  p[0] = tuple(p[1:])

def p_clase_bloque(p):
  ''' 
  clase_bloque :  OCURLY ATTRIBUTES COLON clase_bloque1 METHODS COLON clase_metodos_bloque class_scope_end CCURLY
  '''
  p[0] = tuple(p[1:])

def p_clase_bloque1(p):
  ''' 
  clase_bloque1 : dec
                | empty
  '''  
  p[0] = p[1] 

def p_clase_metodos_bloque(p):
  ''' 
  clase_metodos_bloque : funcion clase_metodos_bloque
                       | empty
  '''
  p[0] = tuple(p[1:])

################################################
# CICLO WHILE
def p_ciclo_while(p):
  '''
  ciclo_while : WHILE cond2 THEN bloque_ciclo SEMICOLON
  '''
  p[0] = tuple(p[1:])

################################################
# CICLO FOR
def p_ciclo_for(p):
  '''
  ciclo_for : FOR OPAREN variable FROM ciclo_for1 TO ciclo_for1 BY ciclo_for1 CPAREN THEN bloque_ciclo SEMICOLON
  '''
  p[0] = tuple(p[1:])


def p_ciclo_for1(p):
  '''
  ciclo_for1 : CSTINT
             | variable
  '''
  p[0] = tuple(p[1:])

 ################################################
# DECLARACION VARS
def p_dec(p):
  '''
  dec : VAR tipo SEMICOLON dec1
  '''
  p[0] = tuple(p[1:])

def p_dec1(p):
  '''
  dec1 : dec
       | empty
  '''
  p[0] = p[1]

################################################
# TIPO
def p_tipo(p):
  '''
  tipo : compuesto ID saw_id saw_variable tipo1
       | simple ID saw_id saw_variable tipo1
       | multiple ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable tipo2
  '''
  p[0] = tuple(p[1:])

def p_tipo1(p):
  '''
  tipo1 : COMMA ID saw_id saw_variable tipo1
        | empty
  '''
  p[0] = tuple(p[1:])

def p_tipo2(p):
  '''
  tipo2 : COMMA ID saw_id OBRACKET CSTINT CBRACKET saw_dimension tipo3 saw_variable
        | empty
  '''
  p[0] = tuple(p[1:])

def p_tipo3(p):
  '''
  tipo3 : OBRACKET CSTINT CBRACKET saw_dimension
        | empty
  '''
  p[0] = tuple(p[1:])

def p_tipo_simple(p):
  '''
  simple : INT saw_type
         | FLOAT saw_type
         | BOOL saw_type
         | STRING saw_type
         | CHAR saw_type
  '''
  p[0] = p[1]

def p_tipo_multiple(p):
  '''
  multiple : INTS saw_type
           | FLOATS saw_type
           | BOOLS saw_type
           | STRINGS saw_type
           | CHARS saw_type
  '''
  p[0] = p[1]

def p_tipo_compuesto(p):
  '''
  compuesto : ID saw_type
            | DATAFRAME saw_type
            | FILE saw_type
  ''' 
  p[0] = p[1]

################################################
# BLOQUE
def p_bloque(p):
  '''
  bloque : OCURLY b1 CCURLY scope_end
  '''
  p[0] = tuple(p[1:])

def p_b1(p):
  '''
  b1 : estatuto b1
     | empty
  '''
  p[0] = tuple(p[1:])

# BLOQUE CICLO
def p_bloque_ciclo(p):
  '''
  bloque_ciclo : OCURLY bc1 CCURLY bc_end
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
  p[0] = p[1]

def p_estatuto_ciclo(p):
  '''
  estatuto_ciclo : asignacion
                 | llamada
                 | condicion
                 | escritura
                 | leer
                 | ciclo_while
                 | ciclo_for
                 | ternaria
                 | dec
  '''
  p[0] = p[1]

def p_estatuto_redux(p):
  '''
  estatuto_redux : asignacion
                 | llamada
                 | escritura
                 | leer
                 | ternaria
  '''
  p[0] = tuple(p[1:])

################################################
# ASIGNACION
def p_asignacion(p):
  '''
  asignacion : variable AS exp saw_asig
  '''
  p[0] = tuple(p[1:])

################################################
# CONDICIONAL
def p_condicion(p):
  '''
  condicion : IF cond2 saw_cond THEN bloque_ciclo cond1 SEMICOLON
  '''
  p[0] = tuple(p[1:])

def p_cond1(p):
  '''
  cond1 : ELSE bloque_ciclo
        | ELSE IF cond2 saw_cond THEN bloque_ciclo cond1
        | empty
  '''
  p[0] = tuple(p[1:])

def p_cond2(p):
  '''
    cond2 : OPAREN exp CPAREN
  '''
  p[0] = tuple(p[1:])

################################################
# condicion ternaria
def p_ternaria(p):
  '''
  ternaria : exp QUESTION estatuto_redux COLON estatuto_redux SEMICOLON
  '''
  p[0] = tuple(p[1:])

################################################
# ESCRITURA
def p_escritura(p):
  '''
  escritura : PRINT OPAREN exp saw_print_exp e1 CPAREN
  '''
  p[0] = tuple(p[1:])

def p_e1(p):
  '''
  e1 : COMMA exp saw_print_exp e1
     | empty
  '''
  p[0] = tuple(p[1:])

################################################
# LEER
def p_leer(p):
  '''
  leer  : READ OPAREN variable saw_read_exp l1 CPAREN
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
# LLAMADA FUNCION
def p_llamada_funcion(p):
  '''
  llamada : ID saw_id OPAREN exp llamada1 CPAREN
          | ID saw_id OPAREN CPAREN
  '''
  p[0] = tuple(p[1:])

def p_llamada_funcion1(p):
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
  if not quadruple.pOper:
    p[0] = quadruple.pilaO.pop()
    #TODO: usar la función getType para tener el tipo final que evalua la expresion y guardarlo
    print('EVALUACION EXPRESION:')
    print(p[0])
    # print('EVALUACION EXPRESION:')
    # print(symbolTable.getCurrentScope().getLatestName())
    # print(symbolTable.getCurrentScope().getLatestType())
    # print(p[0])
    symbolTable.getCurrentScope().setLatestExpValue(p[0])
    quadruple.clearQuad()
 

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
         | variable
         | llamada
  '''
  p[0] = tuple(p[1:])

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : CSTINT saw_end_value_int
         | CSTFLT saw_end_value_flt
         | CSTCHAR 
         | CSTSTRING saw_end_value_str
         | boolean 
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
    print("SYNTAX ERROR! BEFORE THE", p.value , "ON LINE", p.lineno)
  
################################################
# AUX RULES FOR SYMBOL TABLE
def p_saw_program(p):
  ''' saw_program : '''

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
  # POINTS TO EXISTING VARIABLE
  global pointer
  if pointer != False and pointer != None:
    if (pointer.getVarType() == symbolTable.getCurrentScope().getLatestType()):
      pointer.setValue(p[-1])
    else:
      raise Exception("ERROR! Type Mismatch")
      # return False
  pointer = None


def p_saw_end_value_int(p):
  ''' saw_end_value_int : '''
  quadruple.pilaO.append(p[-1])

def p_saw_end_value_flt(p):
  ''' saw_end_value_flt : '''
  quadruple.pilaO.append(p[-1])

def getType(operand):
  if isinstance(operand,bool):
    return 'boo'
  elif isinstance(operand,int):
    return 'int'
  elif isinstance(operand,float):
    return 'flt'
  
def p_saw_end_value_str(p):
  ''' saw_end_value_str : '''
  quadruple.pilaO.append(p[-1])

def p_saw_plusminus_operator(p):
  ''' saw_plusminus_operator  : '''
  quadruple.pOper.append(p[-1])

def p_check_plusminus_operator(p):
  ''' check_plusminus_operator  : '''
  workingStack = quadruple.getWorkingStack()
  res = quadHelpers.check_plusminus_operator(workingStack)

def p_saw_multdiv_operator(p):
  ''' saw_multdiv_operator  : '''
  quadruple.pOper.append(p[-1])

def p_check_multdiv_operator(p):
  ''' check_multdiv_operator  : '''
  workingStack = quadruple.getWorkingStack()
  quadHelpers.check_multdiv_operator(workingStack)

def p_saw_relational_operator(p):
  ''' saw_relational_operator : '''
  quadruple.pOper.append(p[-1])

def p_check_relational_operator(p):
  ''' check_relational_operator : '''
  workingStack = quadruple.getWorkingStack()
  quadHelpers.check_relational_operator(workingStack)

def p_check_and_operator(p):
  '''
  check_and_operator  :
  '''
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '&&':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand) 
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = left_operand and right_operand
        quadruple.pilaO.append(tvalue)
      else:
        return result_Type

def p_check_or_operator(p):
  '''
  check_or_operator :
  '''
  workingStack = quadruple.getWorkingStack()
  if workingStack:
    if workingStack[-1] == '||':
      right_operand = quadruple.pilaO.pop() 
      right_type = getType(right_operand)
      left_operand = quadruple.pilaO.pop()
      left_type = getType(left_operand)
      operator = workingStack.pop()
      if quadruple.pOper:
        quadruple.pOper.pop()
      result_Type = SemanticCube[operator][left_type][right_type]
      
      if result_Type != 'TYPE MISMATCH':
        tvalue = left_operand or right_operand
        quadruple.pilaO.append(tvalue)
      else:
        return result_Type

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

def p_saw_print_exp(p):
  ''' saw_print_exp : '''
  print(symbolTable.getCurrentScope().getLatestExpValue())

def p_saw_read_exp(p):
  ''' saw_read_exp : '''
  # print(symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName()))

def p_saw_cond(p):
  ''' saw_cond : '''
  # print(symbolTable.getCurrentScope().sawCalledVariable(symbolTable.getCurrentScope().getLatestName()))

def p_bc_end(p):
  ''' bc_end : '''

parser = yacc.yacc()

lexer.input(
  '''
  program viendo;
  var ints globales[1];
  var ints globs[12][12];
  var boos matriz[12][12];
  var str strinn, stru;
  var cha c;
  {
    /* Este programa es
    demostracion */

    func int hola(ints globales[20], boo you) {
      /* ints globales[20] */
      var str ha;
      var int a, e, i;
      a = 20
      e = 2 + 2
      
    }

    func boo adios(boos jajas[12], cha si) {
      var str uuuu;
      var int o, w, oo;
      w = 80.1
      o = 12 * 5
      oo = 60/5 
    }
  }
  '''
)

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
      symbolTable.printingAll()
      symbolTable.reset()

    except EOFError:
      print("INCORRECT")
    if not reading: continue
