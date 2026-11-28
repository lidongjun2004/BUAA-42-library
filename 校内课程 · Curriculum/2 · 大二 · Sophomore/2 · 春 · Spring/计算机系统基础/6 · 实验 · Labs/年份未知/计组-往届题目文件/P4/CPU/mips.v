`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:26:38 11/18/2021 
// Design Name: 
// Module Name:    mips 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module mips(
    input clk,
    input reset
    );

wire RegWrite;
wire nPC_sel;
wire MemWrite;
wire ALUScr;
wire SavePC;
wire MemtoReg;
wire [1:0] nPCctr;
wire [1:0] ALUctr;
wire [1:0] ExtOp;
wire [4:0] A1;
wire [4:0] A2;
wire [4:0] A3;
wire [31:0] Instr;
wire [31:0] nPC;
wire [31:0] PC;
wire [31:0] Ext32;
wire [31:0] ALURes;
wire [31:0] WriteData;
wire [31:0] RD1;
wire [31:0] RD2;
wire [31:0] ALU2;
wire [9:0] MemAddr;
wire [31:0] MemIn;
wire [31:0] MemOut;
wire [31:0] RegData;

	BuildPC MyPC(
		.clk			(clk),
		.reset		(reset),
		.nPC_sel		(nPC_sel),
		.nPC			(nPC),
		.PC			(PC));
	BuildGRF MyGRF(
		.clk			(clk),
		.WE			(RegWrite),
		.reset		(reset),
		.A1			(A1),
		.A2			(A2),
		.A3			(A3),
		.PC			(PC),
		.WD			(WriteData),
		.RD1			(RD1),
		.RD2			(RD2));
	BuildALU MyALU(
		.F				(ALUctr),
		.A				(RD1),
		.B				(ALU2),
		.C				(ALURes));
	BuildDM MyDM(
		.clk			(clk),
		.reset		(reset),
		.MemWrite	(MemWrite),
		.Addr			(MemAddr),
		.ALURes		(ALURes),
		.PC			(PC),
		.DataIn		(MemIn),
		.DataOut		(MemOut));
	BuildController MyController(
		.opcode		(Instr[31:26]), 
		.func			(Instr[5:0]), 
		.RegDst		(), 
		.ALUSrc		(ALUScr),
		.MemtoReg	(MemtoReg), 
		.RegWrite	(RegWrite),
		.MemWrite	(MemWrite),
		.nPC_sel		(nPC_sel),
		.ExtOp		(ExtOp),
		.ALUctr		(ALUctr),
		.SavePC		(SavePC),
		.nPCctr		(nPCctr));
	BuildnPC MynPC(
		.PC			(PC),
		.RegData		(RegData),
		.Instr		(Instr),
		.ALURes		(ALURes),
		.nPCctr		(nPCctr),
		.nPC			(nPC));
	BuildEXT MyEXT(
		.Imm16		(Instr[15:0]),
		.ExtOp		(ExtOp),
		.Ext32		(Ext32));
	BuildIM MyIM(
		.PC			(PC),
		.Instr		(Instr));
		
assign ALU2 = (ALUScr == 1) ? Ext32 : RD2;
assign WriteData =	(MemtoReg == 1) ? MemOut :
							(SavePC == 1) ? PC + 4 : ALURes;
assign MemIn = RD2;
assign A1 = Instr[25:21];
assign A2 = Instr[20:16];
assign A3 = (ALUScr == 1) ? A2 :  
				(SavePC == 1) ? 31 : Instr[15:11];
assign MemAddr = ALURes[11:2];
assign RegData = RD1;
endmodule
