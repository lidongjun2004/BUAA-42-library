`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:19:33 11/19/2021 
// Design Name: 
// Module Name:    EXT 
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
module BuildEXT(
    input [15:0] Imm16,
	 input [1:0] ExtOp,
    output [31:0] Ext32
    );

	function [31:0] sign_ext;
		input [15:0] imm;
		
		begin
			if(imm[15] == 1)
			begin
				sign_ext[31:16] = 16'hffff;
				sign_ext[15:0] = imm;
			end
			else
			begin
				sign_ext[31:16] = 16'h0000;
				sign_ext[15:0] = imm;
			end
		end
	endfunction
	
	function [31:0] zero_ext;
		input [15:0] imm;
		
		begin
			zero_ext[31:16] = 16'h0000;
			zero_ext[15:0] = imm;
		end
	endfunction
	
	function [31:0] low_ext;
		input [15:0] imm;
		
		begin
			low_ext[31:16] = imm;
			low_ext[15:0] = 16'h0000;
		end
	endfunction
	
	assign Ext32 = (ExtOp == 2'b00) ? zero_ext(Imm16) :
						(ExtOp == 2'b01) ? sign_ext(Imm16) :
						(ExtOp == 2'b10) ? low_ext(Imm16) : 32'b0;
endmodule
