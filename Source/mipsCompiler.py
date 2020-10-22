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

tokens = ('REGISTER', 'OFFSET', 'LABELDEF', 'LABEL', 'NUMBER', 'MNEMONIC')
