#!/usr/bin/env python3
import ply.lex as lex
import ply.yacc as yacc
from dictionaries import *


tokens = ('IMM', 'REG', 'OFFSET', 'LABELDEF', 'LABEL', 'NUMBER', 'MNEMONIC', 'R', 'J','I', 'O', 'COMA')

t_COMA = r','

labels_def = {}


def t_LABELDEF(t):
    r'\w+:'

    if t.value[:len(t.value)-1] in labels_def.keys():
        # print("Label repetido!")
        return
    else:
        labels_def[t.value[:len(t.value)-1]] = t.lineno
        return t


def t_REG(t):
    r'\$(0|(v|k)[0-1]|a[0-3]|t[0-9]|s[0-7]|at|gp|sp|fp|ra)'
    t.value = getRegisterAddress(t.value[1:])
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

def t_IMM(t):
    r'-?\d+'
    t.value = int(t.value)
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

texto = '''add $s2, $s0, $s1
addu $t2, $t0, $t1
div $s0, $t0
jr $s7
mfhi $s7
mflo $t7
multu $s0, $0
sll $s7, $t0, 10
sllv $s0, $s1, $s2
sra $t9, $t8, 31
'''

lexer = lex.lex()
lexer.input(texto)

while True:
    tok = lexer.token()
    print(tok)
    if not tok:
        break

print(labels_def)

def p_exp_exp(p):
    'exp : exp exp'
    p[0] = (p[1], p[2])

def p_exp(p):
    'exp : inst '
    p[0] = p[1]

def p_exp_label(p):
    'exp : LABELDEF inst '
    p[0] = p[2]

def p_R1(p):
    'inst : R REG COMA REG COMA REG'
    if(p[1] == 'sllv' or p[1] == 'srlv'):
        p[0] = "%s%s%s%s00000%s" % (opcodes[p[1]], p[6], p[4], p[2],func[p[1]])
    else:
        p[0] = "%s%s%s%s00000%s" % (opcodes[p[1]], p[4], p[6], p[2],func[p[1]])

def p_R2(p):
    'inst : R REG COMA REG'
    p[0] = "%s%s%s0000000000%s" % (opcodes[p[1]], p[2], p[4], func[p[1]])

def p_R3(p):
    'inst : R REG'
    if(p[1] == 'jr'):
        p[0] = "%s%s000000000000000%s" % (opcodes[p[1]], p[2], func[p[1]])
    elif(p[1] == 'mfhi' or p[1] == 'mflo'):
        p[0] = "%s0000000000%s00000%s" %(opcodes[p[1]], p[2], func[p[1]])

def p_Rshift(p):
    'inst : R REG COMA REG COMA IMM'
    p[0] = "%s00000%s%s%s%s" %(opcodes[p[1]], p[4], p[2], num2bin(abs(p[6]), 5), func[p[1]])


parser = yacc.yacc()

result = parser.parse(texto)

def evalT(arbol):
    if arbol==None:
        return
    if isinstance(arbol, str):
        if len(arbol)>0:
            print("32'b"+arbol + ';\n') 
            print("32'h"+hex(int(arbol,2))[2:].zfill(8).upper()+';\n')
    elif len(arbol) == 1:
        evalT(arbol[0])
    elif len(arbol) == 2:
        evalT(arbol[0])
        evalT(arbol[1])
    else:
        return

evalT(result)