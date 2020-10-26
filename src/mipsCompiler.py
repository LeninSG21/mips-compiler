#!/usr/bin/env python3
import ply.lex as lex
import ply.yacc as yacc
from dictionaries import *
import sys

tokens = ('IMM', 'REG', 'LABELDEF', 'LABEL', 'R', 'J','I', 'O', 'COMA')

t_COMA = r','

labels_def = {}


def t_LABELDEF(t):
    r'[a-zA-Z]+:'

    if t.value[:len(t.value)-1] in labels_def.keys():
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
        t.type = 'LABEL'
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

t_ignore = r' +'

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
    global inst_count
    inst_count += 1
    if(p[1] == 'sllv' or p[1] == 'srlv'):
        p[0] = "%s%s%s%s00000%s" % (opcodes[p[1]], p[6], p[4], p[2],func[p[1]])
    else:
        p[0] = "%s%s%s%s00000%s" % (opcodes[p[1]], p[4], p[6], p[2],func[p[1]])

def p_R2(p):
    'inst : R REG COMA REG'
    global inst_count
    inst_count += 1
    p[0] = "%s%s%s0000000000%s" % (opcodes[p[1]], p[2], p[4], func[p[1]])

def p_R3(p):
    'inst : R REG'
    global inst_count
    inst_count += 1
    if(p[1] == 'jr'):
        p[0] = "%s%s000000000000000%s" % (opcodes[p[1]], p[2], func[p[1]])
    elif(p[1] == 'mfhi' or p[1] == 'mflo'):
        p[0] = "%s0000000000%s00000%s" %(opcodes[p[1]], p[2], func[p[1]])

def p_Rshift(p):
    'inst : R REG COMA REG COMA IMM'
    global inst_count
    inst_count += 1
    p[0] = "%s00000%s%s%s%s" %(opcodes[p[1]], p[4], p[2], num2bin(abs(p[6]), 5), func[p[1]])


def p_I1(p):
    'inst : I REG COMA REG COMA IMM'
    global inst_count
    inst_count += 1
    if p[1] == 'beq' or p[0] == 'bne':
        p[0]  = "%s%s%s%s" % (opcodes[p[1]], p[2], p[4], num2bin_signed(p[6], 16))
    else:
        p[0] = "%s%s%s%s" % (opcodes[p[1]], p[4], p[2], num2bin_signed(p[6], 16))

def p_I2(p):
    'inst : I REG COMA IMM'
    global inst_count
    inst_count += 1
    if p[1] =='lui':
         p[0]  = "%s00000%s%s" % (opcodes[p[1]], p[2], num2bin_signed(p[4], 16))
    else:
        p[0]  = "%s%s%s%s" % (opcodes[p[1]], p[2], branches[p[1]], num2bin_signed(p[4], 16))

def p_I3(p):
    'inst : I REG COMA IMM  REG '
    global inst_count
    inst_count += 1
    p[0] = "%s%s%s%s" % (opcodes[p[1]], p[5], p[2], num2bin(p[4], 16))

def p_I1Label(p):
    'inst : I REG COMA REG COMA LABEL'
    global inst_count

    if p[6] in labels_def.keys():
        labelDefLine = labels_def[p[6]]
        if labelDefLine > inst_count:
            offset = num2bin(labelDefLine - inst_count - 1, 16)
        else:
            offset = num2bin_signed(labelDefLine - 1 - inst_count, 16)
        if p[1] == 'beq' or p[0] == 'bne':
            p[0]  = "%s%s%s%s" % (opcodes[p[1]], p[2], p[4], offset)
        else:
            p[0] = "%s no puede tener %s como entrada" % (p[1], p[6])
    else: 
        print("No existe el label!")
        p[0] = "LABEL NO DEFINIDO"
    
    inst_count += 1
    

def p_I2Label(p):
    'inst : I REG COMA LABEL'
    global inst_count
    
    if p[4] in labels_def.keys():
        labelDefLine = labels_def[p[4]]
        if labelDefLine > inst_count:
            offset = num2bin(labelDefLine - inst_count - 1, 16)
        else:
            offset = num2bin_signed(labelDefLine - 1 - inst_count, 16)
        if p[1] !='lui':
            p[0]  = "%s%s%s%s" % (opcodes[p[1]], p[2], branches[p[1]], offset)
        else:
            p[0] = "%s no puede tener %s como entrada" % (p[1], p[6])
    else: 
        print("No existe el label!")
        p[0] = "LABEL NO DEFINIDO"
    
    inst_count += 1

def p_J(p):
    'inst : J IMM'
    p[0] = "%s%s" % (opcodes[p[1]], num2bin_signed(p[2], 26))

def p_O(p):
    'inst : O '
    p[0] = others[p[1]]

def p_error(p):
    print("Syntax error in line %d" % (p.lineno//2))

def evalT(arbol):
    if arbol==None:
        return
    if isinstance(arbol, str):
        if len(arbol)>0:
            if writeBin:
                binStr = "32'b"+arbol + ';\n' if svFormat else arbol + '\n'
                binF.write(binStr)
            hexStr = hex(int(arbol,2))[2:].zfill(8).upper()
            hexStr ="32'h"+hexStr+';\n' if svFormat else hexStr + '\n'
            hexF.write(hexStr)

    elif len(arbol) == 1:
        evalT(arbol[0])
    elif len(arbol) == 2:
        evalT(arbol[0])
        evalT(arbol[1])
    else:
        return

def printHelp():
    print('''
Usage: mipsCompiler [OPTION] [FILE]

MIPS Compiler will take a txt file with the assembly code. By default, it will only
generate a file with the same name and .hex extension, which contains the machine 
language in hexadecimal format. With the following options, a binary file can also be
generated, and the format can be set to System Verilog to copy and paste the code
in a test bench (for example)

    -b, creates binary file with the machine code and .bin extension
    -s, sets the output format to System Verilog's format
    -p, prints the teaxt read from the input file

    --help, print the help information

Examples:
    mipsCompiler myFile.txt --> output file: myFile.hex
    mipsCompiler -b myFile.txt --> output files: myFile.hex, myFile.bin
    ''')


if __name__ == "__main__":

    # Flags
    writeBin = False
    svFormat = False
    printText = False

    # Read args
    if len(sys.argv) <= 1:
        print("Missing arguments!")
        exit(0)
    elif len(sys.argv) == 2:
        inputFile = sys.argv[1]
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i][0] == '-':
                if sys.argv[i] == "--help":
                    printHelp()
                    exit(0)
                for j in range(1, len(sys.argv[i])):
                    if sys.argv[i][j] == 'b':
                        writeBin = True
                    elif sys.argv[i][j] == 's':
                        svFormat = True
                    elif sys.argv[i][j] == 'p':
                        printText = True
            else:
                inputFile = sys.argv[i]
    
    # Abrir archivo
    
    archivo = open(inputFile)
    texto = archivo.read()

    if printText:
        print(texto)

    # Crear archivos de escritura
    hexF = open(inputFile.replace('txt', 'hex', 1), 'w')
    if writeBin:
        binF = open(inputFile.replace('txt', 'bin', 1), 'w')

    lexer = lex.lex()
    lexer.input(texto)

    while True:
        tok = lexer.token()
        # print(tok)
        if not tok:
            break

    # print(labels_def)

    inst_count = 1

    parser = yacc.yacc()

    result = parser.parse(texto)

    evalT(result)

    hexF.close()

    if writeBin:
        binF.close()
    
    print("Done")