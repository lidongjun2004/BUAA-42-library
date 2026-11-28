`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:30:00 11/18/2021 
// Design Name: 
// Module Name:    GRF 
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
module BuildGRF(
    input clk,
    input WE,
    input reset,
    input [4:0] A1,
    input [4:0] A2,
    input [4:0] A3,
	 input [31:0] PC,
    input [31:0] WD,
	 input [31:0] Instr,
    output [31:0] RD1,
    output [31:0] RD2
    );

	reg [31:0] Reg [31:0];
	integer i;
	
	initial
	begin
		for(i = 0; i < 32; i = i + 1)
		begin
			Reg[i] <= 32'h000000000;
		end
		Reg[28] <= 32'h1800;
		Reg[29] <= 32'h2ffc;
	end
	
	always@(posedge clk)
	begin
		if(reset == 1)
		begin
			for(i = 0; i < 32; i = i + 1)
			begin
				Reg[i] <= 32'b0;
			end
			Reg[28] <= 32'h1800;
			Reg[29] <= 32'h2ffc;
		end
		else if(WE == 1)
		begin
			Reg[A3] <= WD;
		end
	end
	
	assign RD1 =	(A1 == 5'b0) ? 32'b0 :
						(A1 == A3) ? WD : Reg[A1];
	assign RD2 =	(A2 == 5'b0) ? 32'b0 :
						(A2 == A3) ? WD : Reg[A2];
endmodule
