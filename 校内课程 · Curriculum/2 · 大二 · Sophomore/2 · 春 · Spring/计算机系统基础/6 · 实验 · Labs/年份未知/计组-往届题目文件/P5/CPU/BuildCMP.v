`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:35:47 11/28/2021 
// Design Name: 
// Module Name:    BuildCMP 
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
module BuildCMP(
    input [31:0] RD1,
    input [31:0] RD2,
    output Res
    );

	assign Res = (RD1 == RD2) ? 1 : 0;
endmodule
