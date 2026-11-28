`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:15:23 10/21/2021 
// Design Name: 
// Module Name:    ext 
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
module ext(
    input [15:0] imm,
    input [1:0] EOp,
    output [31:0] ext
    );
	reg [31:0] res;
	
	function [31:0] sign_ext;
		input [15:0] imm;
		begin
			sign_ext[15:0] = imm;
			if(imm[15] == 1)
			begin
				sign_ext[31:16] = 16'hffff;
			end
			else
			begin
				sign_ext[31:16] = 16'h0000;
			end
		end
	endfunction
	
	function [31:0] zero_ext;
		input [15:0] imm;
		begin
			zero_ext[15:0] = imm;
			zero_ext[31:16] = 16'h0000;
		end
	endfunction
	
	always @*
	begin
		if(EOp == 2'b00)
		begin
			res = sign_ext(imm);
		end
		else if(EOp == 2'b01)
		begin
			res = zero_ext(imm);
		end
		else if(EOp == 2'b10)
		begin
			res[31:16] = imm;
			res[15:0] = 16'h0000;
		end
		else
		begin
			res = sign_ext(imm);
			res = res << 2;
		end
	end
	
	assign ext = res;
endmodule
