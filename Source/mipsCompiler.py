#!/usr/bin/env python3
from ..PLY.ply import lex
from dictionaries import *

def twos_comp(num, size):
    if(num>=0):
        return bin(num)[2:].zfill(size)
    else:
        x = 2**(size-1) + num
        return "1" + bin(x)[2:].zfill(size-1)

def num2bin(num, size):
    return bin(num)[2:].zfill(size)

tokens = ('REGISTER', 'OFFSET', 'LABELDEF', 'LABEL', 'NUMBER', 'MNEMONIC', 'R', 'J','I', 'O')

labels_def = {}

def t_LABELDEF(t):
    r'\w+:'

    if t.value[:len(t.value)-1] in labels_def.keys():
        # print("Label repetido!")
        return
    else:
        labels_def[t.value[:len(t.value)-1]] = t.lineno
        return t

def t_MNEMONIC(t):
    r'[a-zA-Z]+'
    if t.value in r_type:
        t.type = 'R'
    elif t.value in i_type:
        t.type = 'I'
    elif t.value  in j_type:
        t.type = 'J'
    elif t.value in others.keys():
        t.type = 'O'
    else:
        return
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = r'( |\t)+'

texto = "addi label:"

lexer = lex.lex()
lexer.input(texto)

while True:
    tok = lexer.token()
    if not tok:
        break