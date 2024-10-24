# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    #test 1:

    b = 1
    a = 1 

    dut.ui_in.value = (b << 4) + a
    dut.uio_in.value = 0 #Opcode ADD
    await ClockCycles(dut.clk, 10)
    dut._log.info(f" 1. b: {b} a: {a} Opcode: ADD, value of input is: {dut.ui_in.value}")
    
    assert dut.uo_out.value == 2 and dut.uio_out.value == 0

    #testing ADD opcode:
    dut._log.info(f"Testing all possible ADD combinations")
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 0 #Opcode ADD
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"ADD case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}, UIO: {dut.uio_out.value}")
            assert dut.uo_out.value == ((a+b) & 15) # SUM
            assert (dut.uio_out.value >> 7) == (((a & 8) >> 3) & ((b & 8) >> 3) & ~(((a+b) & 8) >> 3)) or (~((a & 8) >> 3) & ~((b & 8) >> 3) & (((a+b) & 8) >> 3)) #Overflow
            assert ((dut.uio_out.value & 64) >> 6) == (((a+b) & 16) >> 4) # Carryout
            
    dut._log.info(f"All possible ADD combinations successful, now testing all possible SUB combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 1 #Opcode SUB
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"SUB case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}, UIO: {dut.uio_out.value}")
            assert dut.uo_out.value == ((a-b) & 15) # difference
            assert (dut.uio_out.value >> 7) == (((a & 8) >> 3) & ~((b & 8) >> 3) & ~(((a-b) & 8) >> 3)) or (~((a & 8) >> 3) & ((b & 8) >> 3) & (((a-b) & 8) >> 3)) #Overflow
            assert ((dut.uio_out.value & 64) >> 6) == ((~(a-b) & 16) >> 4) # Carryout
            
    dut._log.info(f"All possible SUB combinations successful, now testing all possible MUL combinations")

    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 2 #Opcode MUL
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"MUL case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert dut.uo_out.value == ((a*b) & 255) # product
            
    dut._log.info(f"All possible MUL combinations successful, now testing all possible DIV combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 3 #Opcode DIV
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"DIV case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            if (b != 0): 
                assert (dut.uo_out.value & 15) == ((a // b) & 15) #Remainder
                assert (dut.uo_out.value >> 4) == ((a % b) & 15) #Quotient
            else:
                assert (dut.uo_out.value & 15) == 0 #Remainder
                assert (dut.uo_out.value >> 4) == 0 #Quotient

    dut._log.info(f"All possible DIV combinations successful, now testing all possible AND combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 4 #Opcode AND
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"AND case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert (dut.uo_out.value & 15) == ((a & b) & 15) # bit-wise and

    dut._log.info(f"All possible AND combinations successful, now testing all possible OR combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 5 #Opcode OR
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"OR case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert (dut.uo_out.value & 15) == ((a | b) & 15) # bit-wise or

    dut._log.info(f"All possible OR combinations successful, now testing all possible XOR combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 6 #Opcode XOR
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"XOR case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert (dut.uo_out.value & 15) == ((a ^ b) & 15) # bit-wise xor

    dut._log.info(f"All possible XOR combinations successful, now testing all possible NOT combinations")
    
    i = 0
    for x in range(0,16):
            a = x
            i = i + 1
            dut.ui_in.value = (a << 4)
            dut.uio_in.value = 7 #Opcode NOT
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"NOT case {i}. a: {a}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert (dut.uo_out.value & 15) == ((~a) & 15) # bit-wise and

    dut._log.info(f"All possible NOT combinations successful, now testing all possible ENC combinations")
    
    i = 0
    for x in range(0,16):
        for y in range(0,16):
            b = x
            a = y
            i = i + 1
            dut.ui_in.value = (a << 4) + b
            dut.uio_in.value = 4 #Opcode AND
            await ClockCycles(dut.clk, 10)
            dut._log.info(f"ENC case {i}. a: {a}, b: {b}, input: {dut.ui_in.value}, output: {dut.uo_out.value}")
            assert (dut.uo_out.value & 255) == (((((a << 4) | b) & 255) ^ 171 ) & 255) # encryption

    dut._log.info(f"All possible ENC combinations successful, finished all possible tests")


    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
