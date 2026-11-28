`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:28:51 12/26/2021 
// Design Name: 
// Module Name:    CP0 
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
`define IM SR[15:10]
`define IE SR[0]
`define EXL SR[1]
`define IP Cause[15:10]
`define BD Cause[31]
module CP0(
	input [4:0] A,
	input [31:0] DataIn,
	input [31:0] PC,
	input [4:0] ExcCode,
	input [5:0] HWInt,
	input WE,
	input EXLClr,
	input clk,
	input reset,
	input	delay,
	output IntReq,
	output [31:0] EPC,
	output [31:0] DataOut
    );
	 
	 reg [31:0] SR;
	 reg [31:0] Cause;
	 reg [31:0] reg_EPC;
	 reg [31:0] PRId;
	 
	 initial
	 begin
		SR 	<= 32'b0;
		Cause	<= 32'b0;
		reg_EPC	<= 32'b0;
		PRId	<= 32'b0;
	 end

	always@(posedge clk)
	begin
		`IP <= HWInt;
		if(reset)
		begin
			SR 	<= 32'b0;
			Cause	<= 32'b0;
			reg_EPC	<= 32'b0;
			PRId	<= 32'b0;
		end
		else if(WE)
		begin
			if(A == 8)
			begin
				PRID <= DataIn;
			end
			else if(A == 12)
			begin
				SR <= DataIn;
			end
			else if(A == 13)
			begin
				Cause <= DataIn;
			end
			else if(A == 14)
			begin
				reg_EPC <= DataIn;
			end
		end
		if(EXLClr)
			`EXL <= 1'b0;
		else if(`IE == 1'b1 && `EXL == 1'b0 && (`IM && HWInt) != 0) //外部中断
		begin
			reg_EPC <= PC;
			`BD <= delay;
			`EXL <= 1'b0;
			Cause[6:2] <= 4'b0;
		end
		else if(`IE == 1'b1 && ExcCode != 0)//内部中断
		begin
		
			reg_EPC <= PC;
			`BD <= delay;
			`EXL <= 1'b0;
			Cause[6:2] <= ExcCode;
		end
	end
	
	assign EPC = (`BD == 1) ? reg_EPC - 4 : reg_EPC ;
	assign IntReq =	(`IE == 1'b1 && `EXL == 1'b0 && (`IM && HWInt) != 0) ? 1 : 
							(`IE == 1'b1 && ExcCode != 0) ? 1 : 0;
	assign DataOut =	(A == 8) ? PRID :
							(A == 12) ? SR : 
							(A == 13) ? Cause :
							(A == 14) ? reg_EPC : 32'h0;
endmodule
