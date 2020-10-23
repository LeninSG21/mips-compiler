func = {
    'add': '100000',
    'addu': '100001',
    'and': '100100',
    'div': '011010',
    'divu': '011011',
    'jr': '001000',
    'mfhi': '010000',
    'mflo':'010010',
    'mult': '011000',
    'multu': '011001',
    'or' : '100101',
    'sll': '000000',
    'sllv': '000100',
    'slt': '101010',
    'sltu': '101011',
    'sra': '000011',
    'srl': '000010',
    'srlv': '000110',
    'sub': '100010',
    'subu':'100011',
    'syscall': '001100',
    'xor': '100110'
}

r_type = ('add', 'addu', 'and', 'div', 'divu', 'jr', 'mfhi', 'mflo', 'mult', 'multu', 'or', 'sll', 'sllv', 'slt', 'slt', 'sra','srl', 'srlv', 'sub', 'subu', 'xor' )
i_type = ('addi', 'addiu', 'andi', 'beq', 'bgez', 'bgezal','bgtz', 'blez', 'bltz', 'bltzal', 'bne', 'lb','lui','lw','ori', 'sb', 'slti', 'sltiu','sw', 'xori')
j_type = ('j', 'jal')
others = {
    'noop': '00000000000000000000000000000000', 
    'syscall': '00000000000000000000000000001100'
}

opcodes = {
    'add': '000000',
    'addi': '001000',
    'addiu':'001001',
    'addu':'000000',
    'and':'000000',
    'andi':'001100',
    'beq': '000100',
    'bgez': '000001',
    'bgezal': '000001',
    'bgtz': '000111',
    'blez': '000110',
    'bltz':'000001',
    'bltzal':'000001',
    'bne': '000101',
    'div':'000000',
    'divu':'000000',
    'j': '000010',
    'jal': '000011',
    'jr':'000000',
    'lb':'100000',
    'lui':'001111',
    'lw': '100011',
    'mfhi': '000000',
    'mflo': '000000',
    'mult': '000000',
    'multu': '000000',
    'or': '000000',
    'ori': '001101',
    'sb': '101000',
    'sll':'000000',
    'sllv': '000000',
    'slt': '000000',
    'slti': '001010',
    'sltiu':'001011',
    'sltu': '000000',
    'sra': '000000',
    'srl': '000000',
    'srlv': '000000',
    'sub': '000000',
    'subu':'000000',
    'sw': '101011',
    'xor':'000000',
    'xori': '001110'
}

registerAdress = {
    "at": '00001',
    'gp': '11100',
    'sp': '11101',
    'fp': '11110',
    'ra': '11111',
    'v0': '00010',
    'v1': '00011',
    'k0': '11010',
    'k1': '11011',
    't8': '11000',
    't9': '11001'
}

def num2bin_signed(num, size):
    if(num>=0):
        return bin(num)[2:].zfill(size)
    else:
        x = 2**(size-1) + num
        return "1" + bin(x)[2:].zfill(size-1)

def num2bin(num, size):
    return bin(num)[2:].zfill(size)

def getRegisterAddress(reg):
    if(reg == '0'):
        return '00000'
    elif (reg in registerAdress.keys()):
        return registerAdress[reg]
    
    num = int(reg[1])
    if(reg[0] == 'a'):
        return num2bin(num+4, 5)
    elif(reg[0] == 't'):
        return num2bin(num+8, 5)
    elif(reg[0] == 's'):
        return num2bin(num+16, 5)