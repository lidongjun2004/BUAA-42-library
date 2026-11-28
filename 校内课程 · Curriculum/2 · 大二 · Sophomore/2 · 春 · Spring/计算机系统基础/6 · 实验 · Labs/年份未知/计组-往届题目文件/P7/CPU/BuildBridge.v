`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:10:04 12/25/2021 
// Design Name: 
// Module Name:    BuildBridge 
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
module BuildBridge(
	input [3:0] WE,
	input [31:0] Addr,
	input [31:0] ReadData_Time0,
	input [31:0] ReadData_Time1,
	input [31:0] ReadData_DM,
	output [31:0] ReadData,
	output [3:0] MemWrite,
	output Time0_Write,
	output Time1_Write
    );
	
	assign MemWrite = (32'h0000 <= Addr && Addr <= 32'h2fff) ? WE : 4'b0;
	assign Time0_Write = (WE != 4'b0000 && 32'h7f00 <= Addr && Addr <= 32'h7f0b) ? 1 : 0;
	assign Time1_Write = (WE != 4'b0000 && 32'h7f10 <= Addr && Addr <= 32'h7f1b) ? 1 : 0;
	assign ReadData =	(32'h0000 <= Addr && Addr <= 32'h2fff) ? ReadData_DM :
							(32'h7f00 <= Addr && Addr <= 32'h7f0b) ? ReadData_Time0:
							(32'h7f10 <= Addr && Addr <= 32'h7f1b) ? ReadData_Time1 : 32'h0;
endmodule
