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
  'then': 'THEN',
  'else' : 'ELSE',
  'do' : 'DO',
  'while' : 'WHILE',
  'for' : 'FOR',
}

# terminals and regEx
tokens = [
  'CSTINT',
  'CSTFLT',
  'CSTSTRING',
  'CSTBOOL',
  'CSTINTS',
  'CSTFLTS',
  'CSTSTRS',
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
  'EQUAL',
  'AS',
  'GT',
  'LT',
  'NE',
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
t_NE = r'\>\<'
t_EQ = r'\<\>'

t_ignore = r' \t'

def t_CSTINT(t):
  r'\d+'
  t.value = int(t.value)
  return t

# def t_CSTINTS(t):
#   r'\d+'
#   t.value = int(t.value)
#   return t

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

# ciclos
# 
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
  loop: WHILE condition_body THEN bloque SEMICOLON
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
    |  ID v2 COLON arr SEMICOLON v3

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
  tipo : INT
       | FLOAT
       | BOOL
       | STRING
       | arr
  '''
  p[0] = p[1]

  def p_arr(p):
    '''
    arr: arr1 ID arr2 SEMICOLON
    '''

  
  def p_arr1(p):
    '''
    arr1: INTS
        | FLOATS
        | STRINGS
        | BOOLS
    '''

  def p_arr2(p):
    '''
    arr2: AS OBRACKET cadena CBRACKET
        | empty
    '''

  def p_cadena(p):
    '''
    cadena: CSTINT cadena_int
          | CSTFLT cadena_flt
          | CSTSTRING cadena_str
          | CSTBOOL cadena_boo
    '''
  
def p_cadena_str(p):
  '''
  cadena_str: COMMA CSTSTRING cadena_str
            | empty
  '''

  
def p_cadena_boo(p):
  '''
  cadena_boo: COMMA CSTBOOL cadena_boo
            | empty
  '''


def p_cadena_int(p):
  '''
  cadena_int: COMMA CSTINT cadena_int
            | empty
  '''

def p_cadena_flt(p):
  '''
  cadena_flt: COMMA CSTFLT cadena_flt
            | empty
  '''
  
# ints jaja = [1, 2, 3, ]
# var tal, tal, tal : int,
# 
################################################
# BLOQUE
def p_bloque(p):
  '''
  bloque : OBRACE b1 CBRACE
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
  '''

################################################
# ASIGNACION
def p_asignacion(p):
  '''
  asignacion : ID AS expresion SEMICOLON
  '''

################################################
# condition
def p_condition(p):
  '''
  condition : IF condition_body THEN bloque cond1 SEMICOLON
  '''

def p_cond1(p):
  '''
  cond1 : ELSE bloque
        | ELSE IF condition_body THEN bloque
        | empty
  '''

def p_condition_body(p):
  '''
    condition_body : OPAREN expresion CPAREN
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
      | O
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
         | PLUS varCST
         | MINUS varCST
         | varCST
  '''

################################################
#VARCST
def p_varcst(p):
  '''
  varcst : ID
         | CSTINT
         | CSTFLT
         | CSTSTRING
         | CSTBOOL
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

# lexer.input(
#     '''
#     program p2021;
#     var even, odd: int; 
#     {
#       if(even > odd) {
#         print("Hello world!");
#       } else {
#         print('Goodbye world.');
#       };
#     }
#     '''
# )

while True:
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

