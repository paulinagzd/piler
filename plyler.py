# Paulina Gonzalez Davalos
# Luis Felipe Miranda Icazbalceta
# A01194111
# A00820799
# Tarea 3.2 con PLY

import ply.lex as lex
import ply.yacc as yacc
import sys

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
  'str' : 'STRING',
  'boo' : 'BOOL',
  'True' : 'TRUE',
  'False' : 'FALSE',
  'ints': 'INTS',
  'flts': 'FLOATS',
  'strs': 'STRINGS',
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
  'dataframe' : 'DATAFRAME'
}

# terminals and regEx
tokens = [
  'CSTINT',
  'CSTFLT',
  'CSTSTRING',
  # 'CSTBOOL', #####################
  'ID',
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
  'EQ'
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

t_ignore = r' '

def t_CSTINT(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_CSTFLT(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_ID(t):
  r'[A-Za-z]([A-Za-z]|[0-9])*'
  t.type = reserved.get(t.value, 'ID')
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
  programa : PROGRAM ID SEMICOLON bloque
           | PROGRAM ID SEMICOLON dec bloque
  '''
  p[0] = 'SUCCESS'

################################################
# FUNCION
def p_funcion(p):
  '''
  funcion : FUNCTION func1 ID OPAREN param CPAREN bloque
  '''

def p_funcion1(p):
  '''
  func1 : simple
        | VOID
  '''

def p_param(p):
  '''
  param : simple ID variable2 param1
        | multiple ID variable1 variable1 variable2 param1
        | empty
  '''

def p_param1(p): ####### OJO
  '''
  param1 : COMMA param
         | empty
  '''

################################################
# CLASE
def p_clase(p):
  '''
    clase : CLASS ID COLON clase_bloque SEMICOLON
  '''

def p_clase_bloque(p):
  ''' 
  clase_bloque :  OCURLY ATTRIBUTES COLON clase_bloque1 METHODS COLON clase_metodos_bloque CCURLY
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
  ciclo_while : WHILE cond2 THEN bloque SEMICOLON
  '''

################################################
# CICLO FOR
def p_ciclo_for(p):
  '''
  ciclo_for : FOR OPAREN variable FROM ciclo_for1 TO ciclo_for1 BY ciclo_for1 CPAREN THEN bloque SEMICOLON
  '''

def p_ciclo_for1(p):
  '''
  ciclo_for1 : CSTINT
             | variable
  '''

 ################################################
# DECLARACION VARS
def p_dec_var(p):
  '''
  dec : VAR tipo SEMICOLON dec1
  '''

def p_dec_var1(p):
  '''
  dec1 : dec
       | empty
  '''

################################################
# TIPO
def p_tipo(p):
  '''
  tipo : compuesto ID tipo1
       | simple ID tipo1
       | multiple ID tipo3 tipo3 tipo2
  '''

def p_tipo1(p):
  '''
  tipo1 : COMMA ID tipo1
        | empty
  '''

def p_tipo2(p):
  '''
  tipo2 : COMMA ID tipo3 tipo3
        | empty
  '''

def p_tipo3(p):
  '''
  tipo3 : OBRACKET CSTINT CBRACKET
        | empty
  '''

def p_tipo_simple(p):
  '''
  simple : INT
         | FLOAT
         | BOOL
         | STRING
  '''
  p[0] = p[1]

def p_tipo_multiple(p):
  '''
  multiple : INTS
           | FLOATS
           | BOOLS
           | STRINGS
  '''
  p[0] = p[1]

def p_tipo_compuesto(p):
  '''
  compuesto : ID
            | DATAFRAME
            | FILE
  '''
  
################################################
# BLOQUE
def p_bloque(p):
  '''
  bloque : OCURLY b1 CCURLY
  '''

def p_b1(p):
  '''
  b1 : estatuto b1
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

################################################
# ASIGNACION
def p_asignacion(p):
  '''
  asignacion : variable AS exp SEMICOLON
  '''

################################################
# CONDICIONAL
def p_condicion(p):
  '''
  condicion : IF cond2 THEN bloque cond1 SEMICOLON
  '''

def p_cond1(p):
  '''
  cond1 : ELSE bloque
        | ELSE IF cond2 THEN bloque
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
  ternaria : exp QUESTION estatuto COLON estatuto SEMICOLON
  '''

################################################
# ESCRITURA
def p_escritura(p):
  '''
  escritura : PRINT OPAREN exp e1 CPAREN SEMICOLON
  '''

def p_e1(p):
  '''
  e1 : COMMA exp e1
     | empty
  '''

################################################
# LEER
def p_leer(p):
  '''
  leer  : READ OPAREN exp e1 CPAREN SEMICOLON
  '''

################################################
# BOOLEAN
def p_boolean(p):
  '''
  boolean : TRUE
          | FALSE
  '''

################################################
# VARIABLE (llamada)
def p_variable(p):
  '''
  variable : ID variable1 variable1 variable2
  '''

def p_variable1(p):
  '''
  variable1 : OBRACKET exp CBRACKET
            | empty
  '''

def p_variable2(p):
  '''
  variable2 : PERIOD ID variable1 variable1 variable2
            | empty 
  '''

################################################
# LLAMADA FUNCION
def p_llamada_funcion(p):
  '''
  llamada : ID OPAREN exp llamada1 CPAREN SEMICOLON
          | ID OPAREN CPAREN SEMICOLON
  '''

def p_llamada_funcion1(p):
  '''
  llamada1 : COMMA exp llamada1
           | empty
  '''

################################################
# EXP
def p_exp(p):
  '''
  exp : texp exp1
  '''

def p_exp1(p):
  '''
  exp1 : OR texp exp1
       | empty
  '''

def p_texp(p):
  '''
  texp : gexp texp1
  '''

def p_texp1(p):
  '''
  texp1 : AND gexp texp1
        | empty
  '''

def p_gexp(p):
  '''
  gexp : mexp gexp1
  '''

def p_gexp1(p):
  '''
  gexp1 : LT mexp
        | GT mexp
        | EQ mexp
        | NE mexp
        | empty
  '''

def p_mexp(p):
  '''
  mexp : termino mexp1
  '''

def p_mexp1(p):
  '''
  mexp1 : PLUS termino mexp1
        | MINUS termino mexp1
        | empty
  '''

################################################
# TERMINO
def p_termino(p):
  '''
  termino : factor term1
  '''

def p_term1(p):
  '''
  term1 : MULT factor term1
        | DIV factor term1
        | empty
  '''

################################################
# FACTOR
def p_factor(p):
  '''
  factor : OPAREN exp CPAREN
         | varcst
         | variable
         | llamada
  '''

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : CSTINT
         | CSTFLT
         | CSTSTRING
         | boolean
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
    print("SYNTAX ERROR! AT")
    print(p)   

################################################

parser = yacc.yacc()

lexer.input(
  '''
  program multi;
  var ints a[12][12];
  {
      a = 4;
      b = 5;
      while ( a < b ) then {
          print('Yay, "ello" kasjkasj');
      };
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

    except EOFError:
      print("INCORRECT")
    if not reading: continue

