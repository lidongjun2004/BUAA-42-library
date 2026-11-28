`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:28:42 11/19/2021 
// Design Name: 
// Module Name:    BuildIM 
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
module BuildIM(
    input [31:0] PC,
    output [31:0] Instr
    );

	reg [31:0] IM [0:1023];
	reg [9:0]index;
	initial
		$readmemh("code.txt", IM);
	
	always@(PC)
		index = (PC - 32'h00003000)/ 4;
	assign Instr = IM[index];
endmodule
