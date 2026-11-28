`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:07:34 12/16/2021 
// Design Name: 
// Module Name:    BE 
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
module BE(
	input MemWrite,
   input [1:0] MemAddrCtr,
   input [31:0] ALURes,
	input [31:0] MemIn,
   output [3:0] Byteen,
	output [31:0] MemOut
   );
	 
	assign Byteen =	(MemWrite == 0) ? 4'b0000 : 
							(MemAddrCtr == 2'b00) ? 4'b1111 : 
							(MemAddrCtr == 2'b01 && ALURes[1] == 1'b0) ? 4'b0011 : 
							(MemAddrCtr == 2'b01 && ALURes[1] == 1'b1) ? 4'b1100 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b00) ? 4'b0001 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b01) ? 4'b0010 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b10) ? 4'b0100 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b11) ? 4'b1000 : 4'b0000;
							
	assign MemOut =	(MemAddrCtr == 2'b01 && ALURes[1] == 1'b1) ? MemIn << 16 :
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b01) ? MemIn << 8 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b10) ? MemIn << 16 : 
							(MemAddrCtr == 2'b10 && ALURes[1:0] == 2'b11) ? MemIn << 24 : MemIn;
endmodule
