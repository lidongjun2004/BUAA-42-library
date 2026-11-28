`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:02:29 11/18/2021 
// Design Name: 
// Module Name:    BuildPC 
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
module BuildPC(
    input clk,
    input reset,
    input nPC_sel,
    input [31:0] nPC,
    output [31:0] PC
    );

	reg [31:0] PCreg;
	
	initial
	begin
		PCreg <= 32'h3000;
	end
	
	always@(posedge clk)
	begin
		if(reset == 1)
			PCreg <= 32'h3000;
		else if(nPC_sel == 1)
			PCreg <= nPC;
		else
			PCreg <= PCreg + 4;
	end
	
	assign PC = PCreg;
endmodule
