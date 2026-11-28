`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:49:03 11/25/2021 
// Design Name: 
// Module Name:    BuildIF-ID 
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
module BuildIFID(
    input clk,
	 input reset,
	 input Stall,
	 input [31:0] InstrIn,
    input [31:0] PCIn,
    output [31:0] InstrOut,
    output [31:0] PCOut
    );
	
	reg [31:0] Instr;
	reg [31:0] PC;
	
	//寄存器需置零防止初始时存储数据
	initial
	begin
		Instr <= 32'b0;
		PC <= 32'b0;
	end
	
	//流水线寄存器
	//Instr存储指令，用于控制
	//PC存储PC值，用于跳转
	always @(posedge clk)
	begin
		if(reset == 1)
		begin
			Instr <= 32'b0;
			PC <= 32'b0;
		end
		else if(Stall == 1)
		begin
			Instr <= Instr;
			PC <= PC;
		end
		else
		begin
			Instr <= InstrIn;
			PC <= PCIn;
		end
	end
	
	assign InstrOut = Instr;
	assign PCOut = PC;
endmodule
