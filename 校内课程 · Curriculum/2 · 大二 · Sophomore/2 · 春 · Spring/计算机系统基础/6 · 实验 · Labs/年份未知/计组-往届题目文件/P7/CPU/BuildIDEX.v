`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:26:55 11/25/2021 
// Design Name: 
// Module Name:    BuildIDEX 
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
module BuildIDEX(
   input clk,
	input reset,
	input [31:0] Instr_In,
   input [31:0] PC_In,
	input [31:0] RD1_In,
	input [31:0] RD2_In,
	input [31:0] Imm_In,
	input RegWrite_In,
	input MemWrite_In,
	input MemtoReg_In,
	input SavePC_In,
	input ALUSrc_In,
	input [3:0] ALUCtr_In,
	input [4:0] Addr_In,
	input [1:0] Tnew_In,
	input Lui_In,
	input ALUSign_In,
	input MemExtOp_In,
	input [1:0] MemAddrCtr_In,
	input [2:0] MDCtr_In,
	input MD_In,
	input ShiftImm_In,
	input CP0_Write_In,
	input CP0_Read_In,
	input BJ_In,
	input [4:0] ExcCode_In,
   output [31:0] Instr_Out,
   output [31:0] PC_Out,
	output [31:0] RD1_Out,
	output [31:0] RD2_Out,
	output [31:0] Imm_Out,
	output RegWrite_Out,
	output MemWrite_Out,
	output MemtoReg_Out,
	output SavePC_Out,
	output ALUSrc_Out,
	output [3:0] ALUCtr_Out,
	output [4:0] Addr_Out,
	output [1:0] Tnew_Out,
	output Lui_Out,
	output ALUSign_Out,
	output MemExtOp_Out,
	output [1:0] MemAddrCtr_Out,
	output [2:0] MDCtr_Out,
	output MD_Out,
	output ShiftImm_Out,
	output CP0_Write_Out,
	output CP0_Read_Out,
	output BJ_Out,
	output [4:0] ExcCode_Out
    );

	reg [31:0] Instr;
	reg [31:0] PC;
	reg [31:0] RD1;
	reg [31:0] RD2;
	reg [31:0] Imm;
	reg RegWrite;
	reg MemWrite;
	reg MemtoReg;
	reg SavePC;
	reg ALUSrc;
	reg [3:0] ALUCtr;
	reg [4:0] Addr;
	reg [1:0] Tnew;
	reg Lui;
	reg ALUSign;
	reg MemExtOp;
	reg [1:0] MemAddrCtr;
	reg [2:0] MDCtr;
	reg MD;
	reg ShiftImm;
	reg CP0_Read;
	reg CP0_Write;
	reg BJ;
	reg [4:0] ExcCode;

	//初始化防止开始时产生写入信号
	initial
	begin
		Instr			<= 32'b0;
		PC				<= 32'b0;
		RD1			<= 32'b0;
		RD2			<= 32'b0;
		Imm			<= 32'b0;
		RegWrite		<= 1'b0;
		MemWrite		<= 1'b0;
		MemtoReg		<= 1'b0;
		SavePC		<= 1'b0;
		ALUSrc		<= 1'b0;
		ALUCtr		<= 4'b0;
		Addr			<= 5'b0;
		Tnew			<= 2'b0;
		Lui 			<= 1'b0;
		ALUSign		<= 1'b0;
		MemExtOp		<= 1'b0;
		MemAddrCtr	<= 2'b00;
		MD				<= 1'b0;
		MDCtr			<= 3'b0;
		ShiftImm		<= 1'b0;
		CP0_Read		<= 1'b0;
		CP0_Write	<= 1'b0;
		BJ				<= 1'b0;
		ExcCode		<= 5'b0;
	end
	
	always @(posedge clk)
	begin
		if(reset == 1)
		begin
			Instr			<= 32'b0;
			PC				<= 32'b0;
			RD1			<= 32'b0;
			RD2			<= 32'b0;
			Imm			<= 32'b0;
			RegWrite		<= 1'b0;
			MemWrite		<= 1'b0;
			MemtoReg		<= 1'b0;
			SavePC		<= 1'b0;
			ALUSrc		<= 1'b0;
			ALUCtr		<= 4'b0;
			Addr			<= 5'b0;
			Tnew			<= 2'b0;
			Lui			<= 1'b0;
			ALUSign		<= 1'b0;
			MemExtOp		<= 1'b0;
			MemAddrCtr	<= 2'b00;
			MD				<= 1'b0;
			MDCtr			<= 3'b0;
			ShiftImm		<= 1'b0;
			CP0_Read		<= 1'b0;
			CP0_Write	<= 1'b0;
			BJ				<= 1'b0;
			ExcCode		<= 5'b0;
		end
		else
		begin
			Instr			<= Instr_In;
			PC				<= PC_In;
			RD1			<= RD1_In;
			RD2			<= RD2_In;
			Imm			<= Imm_In;
			RegWrite		<= RegWrite_In;
			MemWrite		<= MemWrite_In;
			MemtoReg		<= MemtoReg_In;
			SavePC		<= SavePC_In;
			ALUSrc		<= ALUSrc_In;
			ALUCtr		<= ALUCtr_In;
			Addr			<= Addr_In;
			Tnew			<= Tnew_In;
			Lui			<= Lui_In;
			ALUSign		<= ALUSign_In;
			MemExtOp		<= MemExtOp_In;
			MemAddrCtr	<= MemAddrCtr_In;
			MD				<= MD_In;
			MDCtr			<= MDCtr_In;
			ShiftImm		<= ShiftImm_In;
			CP0_Read		<= CP0_Read_In;
			CP0_Write	<= CP0_Write_In;
			BJ				<= BJ_In;
			ExcCode		<= ExcCode_In;
		end
	end
	
	assign Instr_Out		= Instr;
	assign PC_Out			= PC;
	assign RD1_Out			= RD1;
	assign RD2_Out			= RD2;
	assign Imm_Out			= Imm;
	assign RegWrite_Out	= RegWrite;
	assign MemWrite_Out	= MemWrite;
	assign MemtoReg_Out	= MemtoReg;
	assign SavePC_Out		= SavePC;
	assign ALUSrc_Out		= ALUSrc;
	assign ALUCtr_Out		= ALUCtr;
	assign Addr_Out		= Addr;
	assign Tnew_Out		= $signed($signed(Tnew) - $signed(1));
	assign Lui_Out			= Lui;
	assign ALUSign_Out	= ALUSign;
	assign MemExtOp_Out	= MemExtOp;
	assign MemAddrCtr_Out= MemAddrCtr;
	assign MD_Out			= MD;
	assign MDCtr_Out		= MDCtr;
	assign ShiftImm_Out	= ShiftImm;
	assign CP0_Read_Out	= CP0_Read;
	assign CP0_Write_Out = CP0_Write;
	assign BJ_Out			= BJ;
	assign ExcCode_Out	= ExcCode;
endmodule