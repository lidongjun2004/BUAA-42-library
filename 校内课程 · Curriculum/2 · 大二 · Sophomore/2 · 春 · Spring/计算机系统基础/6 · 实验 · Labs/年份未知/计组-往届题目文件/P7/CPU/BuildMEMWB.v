`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:17:08 11/26/2021 
// Design Name: 
// Module Name:    BuildMEMWB 
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
module BuildMEMWB(
	input clk,
	input reset,
	input [31:0] Instr_In,
   input [31:0] PC_In,
	input RegWrite_In,
	input MemtoReg_In,
	input SavePC_In,
	input [31:0] MemData_In,
	input [31:0] ALURes_In,
	input [4:0] Addr_In,
	input [1:0] Tnew_In,
	input BJ_In,
   output [31:0] Instr_Out,
   output [31:0] PC_Out,
	output RegWrite_Out,
	output MemtoReg_Out,
	output SavePC_Out,
	output [31:0] MemData_Out,
	output [31:0] ALURes_Out,
	output [4:0] Addr_Out,
	output [1:0] Tnew_Out,
	output BJ_Out
    );
	 
	reg [31:0] Instr;
   reg [31:0] PC;
	reg RegWrite;
	reg MemtoReg;
	reg SavePC;
	reg [31:0] MemData;
	reg [31:0] ALURes;
	reg [4:0] Addr;
	reg [1:0] Tnew;
	reg BJ;
	
	//初始化为零以防止开始时产生写入数据
	initial
	begin
		Instr		<= 32'b0;
		PC			<= 32'b0;
		RegWrite	<= 1'b0;
		MemtoReg	<=	1'b0;
		SavePC	<= 1'b0;
		MemData	<=	32'b0;
		ALURes	<= 32'b0;
		Addr		<= 5'b0;
		Tnew		<= 2'b0;
		BJ			<= 1'b0;
	end
	
	always @(posedge clk)
	begin
		if(reset == 1)
		begin
			Instr		<= 32'b0;
			PC			<= 32'b0;
			RegWrite	<= 1'b0;
			MemtoReg	<=	1'b0;
			SavePC	<= 1'b0;
			MemData	<=	32'b0;
			ALURes	<= 32'b0;
			Addr		<= 5'b0;
			Tnew		<= 2'b0;
			BJ			<= 1'b0;
		end
		else
		begin
			Instr		<= Instr_In;
			PC			<= PC_In;
			RegWrite	<= RegWrite_In;
			MemtoReg	<=	MemtoReg_In;
			SavePC	<= SavePC_In;
			MemData	<=	MemData_In;
			ALURes	<= ALURes_In;
			Addr		<= Addr_In;
			Tnew		<= Tnew_In;
			BJ			<= BJ_In;
		end
	end
	
	assign Instr_Out		= Instr;
	assign PC_Out			= PC;
	assign RegWrite_Out	= RegWrite;
	assign MemtoReg_Out	= MemtoReg;
	assign SavePC_Out		= SavePC;
	assign MemData_Out	= MemData;
	assign ALURes_Out		= ALURes;
	assign Addr_Out		= Addr;
	assign Tnew_Out		= $signed($signed(Tnew) - $signed(1));
	assign BJ_Out			= BJ;
endmodule
