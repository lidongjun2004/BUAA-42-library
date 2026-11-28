`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:06:07 12/16/2021 
// Design Name: 
// Module Name:    BuildCmp 
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
module BuildCmp(
    input [31:0] Cmp1,
    input [31:0] Cmp2,
    input [2:0] BCtr,
    input [2:0] nPCCtr,
    output nPCsel
    );

	assign nPCsel =	(nPCCtr == 3'b000) ? 
							((BCtr == 3'b000 && Cmp1 == Cmp2) ? 1'b1 :
							(BCtr == 3'b001 && Cmp1 != Cmp2) ? 1'b1 :
							(BCtr == 3'b010 && $signed(Cmp1) <= $signed(0)) ? 1'b1 :
							(BCtr == 3'b011 && $signed(Cmp1) < $signed(0)) ? 1'b1 : 
							(BCtr == 3'b100 && $signed(Cmp1) >= $signed(0)) ? 1'b1 :
							(BCtr == 3'b101 && $signed(Cmp1) > $signed(0)) ? 1'b1 : 1'b0) : 1'b0;
endmodule
