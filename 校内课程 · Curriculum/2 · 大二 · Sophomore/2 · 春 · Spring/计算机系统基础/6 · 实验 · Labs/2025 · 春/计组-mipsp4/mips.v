`timescale 1ns / 1ps
`default_nettype none
module mips (
	input wire clk,
	input wire reset
);
	wire pcWriteEnable;
	wire[31:0] pcWriteData,pc,opcode;
	A_IFU ifu(
		.clk(clk),
		.reset(reset),
		.pcWriteEnable(pcWriteEnable),
		.pcWriteData(pcWriteData),
		.pc(pc),
		.opcode(opcode)
	);
	wire[4:0] regRead1Address,regRead2Address,regWriteId;
	wire regWriteEnable;
	wire[31:0] regWriteData,regRead1Data,regRead2Data;
	B_RegisterFile grf(
		.clk(clk),
		.reset(reset),
		.pc(pc),
		.read1Address(regRead1Address),
		.read2Address(regRead2Address),
		.writeEnable(regWriteEnable),
		.writeAddress(regWriteId),
		.writeData(regWriteData),
		.read1Data(regRead1Data),
		.read2Data(regRead2Data)
	);
	wire memoryReadEnable,memoryWriteEnable;
	wire[31:0] memoryAddress,memoryWriteData,memoryReadData;
	D_DM dm(
		.clk(clk),
		.reset(reset),
		.pc(pc),
		.memoryReadEnable(memoryReadEnable),
		.memoryWriteEnable(memoryWriteEnable),
		.memoryAddress(memoryAddress),
		.memoryWriteData(memoryWriteData),
		.memoryReadData(memoryReadData)
	);
	wire [4:0] rs5,rt5;
	B_Decoder decoder(
		.pc(pc),
		.opcode(opcode),
		.rs5(regRead1Address),
		.rt5(regRead2Address)
	);
	C_ALU alu(
		.clk(clk),
		.pc(pc),
		.opcode(opcode),
		.rsVal(regRead1Data),
		.rtVal(regRead2Data),
		.regWriteEnable(regWriteEnable),
		.regWriteId(regWriteId),
		.regWriteData(regWriteData),
		.pcWriteEnable(pcWriteEnable),
		.pcWriteData(pcWriteData),
		.memoryAddress(memoryAddress),
		.memoryReadEnable(memoryReadEnable),
		.memoryReadInputData(memoryReadData),
		.memoryWriteEnable(memoryWriteEnable),
		.memoryWriteOutputData(memoryWriteData)
	);
endmodule