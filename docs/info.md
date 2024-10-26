<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This 4-bit ALU works by taking an 8-bit input, which is split in half to serve as two 4-bit inputs. The 4 Least Significant Bits (LSBs)
of the 8-bit input is considered b, while the 4 Most Significant Bits (MSBs) of the 8-bit input is considered a. To select which operation to do, change the 4 LSBs of the uio_in to the desired opcode:

0 - 0000 - ADD: a + b; in uio_out, the MSB represents the overflow flag and the 2nd MSB represents the carryout flag
1 - 0001 - SUB: a - b; in uio_out, the MSB represents the overflow flag and the 2nd MSB represents the carryout flag
2 - 0010 - MUL: a * b; 
3 - 0011 - DIV: a / b; in ui_out, the 4 MSBs represent the quotient and the 4LSBs represent the remainder. If b is 0 then output is 0
4 - 0100 - AND: a & b; output is the bitwise and operation of a and b
5 - 0101 - OR: a | b; output is the bitwise or operation of a and b
6 - 0110 - XOR: a ^ b; output is the bitwise xor operation of a and b
7 - 0111 - NOT: ~a; input only consists of the 4 MSBs of ui_in. Output is the not operation of a and is returned in the 4 LSB of ui_out
8 - 1000 - ENC: encrypts the ui_in bitstream via XORing the bitstream with an encryption key bitstream.

## How to test

To test, set the 4 MSBs of ui_in as your 4-bit number, a, and set the 4 LSBs of ui_in as your 4-bit number, b. Set the 4 LSBs of uio_in as your desired opcode from the above mentioned. ui_out will contain the output and for opcodes ADD and SUB, uio_out will contain overflow and carryout flag in the 2 MSBs respectively.

Overflow signifies if the sign changes during an operation in which the resulting sum or difference is the incorrect sign (positive or negative).

Carryout signifies that the resulting sum or difference is larger than 255 (now a 9-bit number)


## External hardware
No external hardware is required.
