`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:16:53 11/26/2021 
// Design Name: 
// Module Name:    BuildEXMEM 
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
module BuildEXMEM(
   input clk,
	input reset,
	input [31:0] Instr_In,
   input [31:0] PC_In,
	input RegWrite_In,
	input MemWrite_In,
	input MemtoReg_In,
	input SavePC_In,
	input ALUSrc_In,
	input [31:0] ALURes_In,
	input [4:0] Addr_In,
	input [1:0] Tnew_In,
	input [31:0] RD2_In,
	input [1:0] MemAddrCtr_In,
	input MemExtOp_In,
	input CP0_Write_In,
	input CP0_Read_In,
	input BJ_In,
	input [4:0] ExcCode_In,
   output [31:0] Instr_Out,
   output [31:0] PC_Out,
	output RegWrite_Out,
	output MemWrite_Out,
	output MemtoReg_Out,
	output SavePC_Out,
	output ALUSrc_Out,
	output [31:0] RD2_Out,
	output [31:0] ALURes_Out,
	output [4:0] Addr_Out,
	output [1:0] Tnew_Out,
	output [1:0] MemAddrCtr_Out,
	output MemExtOp_Out,
	output CP0_Write_Out,
	output CP0_Read_Out,
	output BJ_Out,
	output [4:0] ExcCode_Out
    );

	reg [31:0] Instr;
	reg [31:0] PC;
	reg RegWrite;
	reg MemWrite;
	reg MemtoReg;
	reg SavePC;
	reg ALUSrc;
	reg [31:0] ALURes;
	reg [4:0] Addr;
	reg [31:0] RD2;
	reg [1:0] Tnew;
	reg [1:0] MemAddrCtr;
	reg MemExtOp;
	reg CP0_Read;
	reg CP0_Write;
	reg BJ;
	reg [4:0] ExcCode;

	//初始化防止开始时产生写入信号
	initial
	begin
		Instr			<= 32'b0;
		PC				<= 32'b0;
		RegWrite		<= 1'b0;
		MemWrite		<= 1'b0;
		MemtoReg		<= 1'b0;
		SavePC		<= 1'b0;
		ALUSrc		<= 1'b0;
		ALURes		<= 32'b0;
		Addr			<= 5'b0;
		Tnew			<= 2'b0;
		RD2			<= 32'b0;
		MemAddrCtr	<= 2'b00;
		MemExtOp		<= 1'b0;
		CP0_Read		<= 1'b0;
		CP0_Write	<= 1'b0;
		BJ				<= 1'b0;
		ExcCode		<= 5'b0;
	end
	
	always @(posedge clk)
	begin
		if(reset == 1)
		begin
			Instr		<= 32'b0;
			PC			<= 32'b0;
			RegWrite	<= 1'b0;
			MemWrite	<= 1'b0;
			MemtoReg	<= 1'b0;
			SavePC	<= 1'b0;
			ALUSrc	<= 1'b0;
			ALURes	<= 32'b0;
			Addr		<= 5'b0;
			Tnew		<= 2'b0;
			RD2		<= 32'b0;
			MemAddrCtr	<= 2'b00;
			MemExtOp		<= 1'b0;
			CP0_Read		<= 1'b0;
			CP0_Write	<= 1'b0;
			BJ				<= 1'b0;
			ExcCode		<= 5'b0;
		end
		else
		begin
			Instr			<= Instr_In;
			PC				<= PC_In;
			RegWrite		<= RegWrite_In;
			MemWrite		<= MemWrite_In;
			MemtoReg		<= MemtoReg_In;
			SavePC		<= SavePC_In;
			ALUSrc		<= ALUSrc_In;
			ALURes		<= ALURes_In;
			Addr			<= Addr_In;
			Tnew			<= Tnew_In;
			RD2			<= RD2_In;
			MemAddrCtr	<= MemAddrCtr_In;
			MemExtOp		<= MemExtOp_In;
			CP0_Read		<= CP0_Read_In;
			CP0_Write	<= CP0_Write_In;
			BJ				<= BJ_In;
			ExcCode		<= ExcCode_In;
		end
	end
	
	assign Instr_Out			= Instr;
	assign PC_Out				= PC;
	assign RegWrite_Out		= RegWrite;
	assign MemWrite_Out		= MemWrite;
	assign MemtoReg_Out		= MemtoReg;
	assign SavePC_Out			= SavePC;
	assign ALUSrc_Out			= ALUSrc;
	assign ALURes_Out			= ALURes;
	assign Addr_Out			= Addr;
	assign Tnew_Out			= $signed($signed(Tnew) - $signed(1));
	assign RD2_Out				= RD2;
	assign MemAddrCtr_Out	= MemAddrCtr;
	assign MemExtOp_Out		= MemExtOp;
	assign CP0_Read_Out		= CP0_Read;
	assign CP0_Write_Out 	= CP0_Write;
	assign BJ_Out				= BJ;
	assign ExcCode_Out		= ExcCode;
endmodule
