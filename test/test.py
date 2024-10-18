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

    dut.ui_in.value = (b>>8) + a
    dut.uio_in.value = 0 #Opcode ADD
    await ClockCycles(dut.clk, 10)
    dut._log.info(f" 1. b: {b} a: {a} Opcode: ADD, value of input is: {dut.ui_in.value}")
    dut._log.info(f" value of output is {dut.ou_out.value}.")
    assert dut.uo_out.value == 2 and dut.uio_out.value == 0

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
