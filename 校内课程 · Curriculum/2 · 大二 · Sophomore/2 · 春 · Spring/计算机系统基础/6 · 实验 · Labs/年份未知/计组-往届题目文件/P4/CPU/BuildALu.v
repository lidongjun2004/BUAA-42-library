`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:17:59 11/18/2021 
// Design Name: 
// Module Name:    BuildALU
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
module BuildALU(
    input [1:0] F,
    input [31:0] A,
    input [31:0] B,
    output [31:0] C
    );

	assign C =	(F == 2'b00) ? A + B :
					(F == 2'b01) ? A - B :
					(F == 2'b10) ? A | B : 0;
endmodule
