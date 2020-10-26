# MIPS Compiler

This translator was built with [Python Lex - Yacc](https://www.dabeaz.com/ply/). It supports the operations that are included in the pdf file MIPS R3000 Instruction Reference.

## Usage

`mipsCompiler [OPTION] [FILE]`

MIPS Compiler will take a txt file with the assembly code. By default, it will only
generate a file with the same name and .hex extension, which contains the machine
language in hexadecimal format. With the following options, a binary file can also be
generated, and the format can be set to System Verilog to copy and paste the code
in a test bench (for example)

| Option | function                                                     |
| ------ | ------------------------------------------------------------ |
| -b     | creates binary file with the machine code and .bin extension |
| -s     | sets the output format to System Verilog's format            |
| -p     | prints the teaxt read from the input file                    |
| --help | print the help information                                   |
