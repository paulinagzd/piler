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
  'print' : 'PRINT',
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
  'while' : 'WHILE'
}

# terminals and regEx
tokens = [
  'CSTINT',
  'CSTFLT',
  'CSTSTRING',
  'CSTBOOL', #####################
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
  'COMMA',
  'COLON',
  'SEMICOLON',
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
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
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
           | PROGRAM ID SEMICOLON vars bloque
  '''
  p[0] = 'SUCCESS'

################################################
def p_loop(p):
  '''
  loop : WHILE cond2 THEN bloque SEMICOLON
  '''

################################################
# VARS
def p_vars(p):
  '''
  vars : VAR v1
  '''

def p_v1(p):
  '''
  v1 : ID v2 COLON tipo SEMICOLON v3 
  '''

def p_v2(p):
  '''
  v2 : COMMA ID v2
     | empty 
  '''

def p_v3(p):
  '''
  v3 : v1
     | empty
  '''

################################################
# TIPO
def p_tipo(p):
  '''
  tipo : unitario
       |  multiple
  '''

def p_unitario(p):
  '''
  unitario : INT
           | FLOAT
           | BOOL
           | STRING
  '''
  p[0] = p[1]

def p_multiple(p):
  '''
  multiple : INTS
           | FLOATS
           | BOOLS
           | STRINGS
  '''
  p[0] = p[1]

def p_arr(p):
  '''
  arr : OBRACKET cadena CBRACKET
      | empty
  '''

def p_cadena(p):
  '''
  cadena : CSTINT cadena_int
         | CSTFLT cadena_flt
         | CSTSTRING cadena_str
         | CSTBOOL cadena_boo
  '''

def p_cadena_int(p):
  '''
  cadena_int : COMMA CSTINT cadena_int
             | empty
  '''

def p_cadena_flt(p):
  '''
  cadena_flt : COMMA CSTFLT cadena_flt
             | empty
  '''

def p_cadena_str(p):
  '''
  cadena_str : COMMA CSTSTRING cadena_str
             | empty
  '''
  
def p_cadena_boo(p):
  '''
  cadena_boo : COMMA CSTBOOL cadena_boo
             | empty
  '''
  
# ints jaja = [1, 2, 3, ]
# var tal, tal, tal : int,
# 
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
           | condition
           | escritura
           | loop
  '''

################################################
# ASIGNACION
def p_asignacion(p):
  '''
  asignacion : ID AS asi1 SEMICOLON
  '''

def p_asi1(p):
  '''
  asi1 : expresion
       | CSTSTRING
       | boolean
       | arr
  '''

################################################
# condition
def p_condition(p):
  '''
  condition : IF cond2 THEN bloque cond1 SEMICOLON
  '''

def p_cond1(p):
  '''
  cond1 : ELSE bloque
        | ELSE IF cond2 THEN bloque
        | empty
  '''

def p_cond2(p):
  '''
    cond2 : OPAREN expresion CPAREN
  '''

################################################
# ESCRITURA
def p_escritura(p):
  '''
  escritura : PRINT OPAREN expresion e1 CPAREN SEMICOLON
            | PRINT OPAREN CSTSTRING e1 CPAREN SEMICOLON
  '''

def p_e1(p):
  '''
  e1 : COMMA expresion e1
     | COMMA CSTSTRING e1
     | empty
  '''

################################################
# BOOLEAN
def p_boolean(p):
  '''
  boolean : TRUE
          | FALSE
  '''

################################################
# EXPRESION
def p_expresion(p):
  '''
  expresion : exp
            | exp LT exp
            | exp GT exp
            | exp NE exp
            | exp EQ exp
  '''

################################################
# EXP
def p_exp(p):
  '''
  exp : termino exp1
  '''

def p_exp1(p):
  '''
  exp1 : PLUS exp
       | MINUS exp
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
  term1 : MULT termino
        | DIV termino
        | empty
  '''

################################################
# FACTOR
def p_factor(p):
  '''
  factor : OPAREN expresion CPAREN
         | PLUS varcst
         | MINUS varcst
         | varcst
  '''

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : ID
         | CSTINT
         | CSTFLT
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
  var a, b, c : ints;
  d, e, f : flt;
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

