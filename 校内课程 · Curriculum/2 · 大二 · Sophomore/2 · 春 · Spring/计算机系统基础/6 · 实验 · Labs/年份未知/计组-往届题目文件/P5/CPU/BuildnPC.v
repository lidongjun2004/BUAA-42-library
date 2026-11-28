`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:50:44 11/19/2021 
// Design Name: 
// Module Name:    BuildnPC 
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
module BuildnPC(
    input [31:0] PC,
    input [31:0] RegData,
    input [31:0] Instr,
    input [2:0] nPCctr,
    output [31:0] nPC
    );
	
	function [31:0] beq_ext;
		input [15:0] offset;
		
		begin
			if(offset[15] == 1)
			begin
				beq_ext[31:18] = 14'h3fff;
				beq_ext[17:2] = offset;
				beq_ext[1:0] = 2'b00;
			end
			else
			begin
				beq_ext[31:18] = 14'h0000;
				beq_ext[17:2] = offset;
				beq_ext[1:0] = 2'b00;
			end
		end
	endfunction
	
	//2'b00 beq,2'b01 jal,2'b10 jr,2'b11 j
	assign nPC =	(nPCctr == 3'b00) ? PC + 4 + beq_ext(Instr[15:0]):
						(nPCctr == 3'b01) ? {PC[31:28], Instr[25:0], 2'b00}:
						(nPCctr == 3'b10) ? RegData :
						(nPCctr == 3'b11) ? {PC[31:28], Instr[25:0], 2'b00}:32'h00003000;
endmodule
