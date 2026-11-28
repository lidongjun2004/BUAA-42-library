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
	 
	function OverFlow;
	input [31:0] A;
	input [31:0] B;
	reg [32:0] tmp1;
	reg [32:0] tmp2;
	reg [32:0] ans;
	
	begin
		tmp1[31:0] = A;
		tmp2[31:0] = B;
		tmp1[32] = A[31];
		tmp2[32] = B[31];
		ans = tmp1 + tmp2;
		if(ans[32:31] == 2'b01 || ans[32:31] == 2'b10)
			OverFlow = 1'b1;
		else
			OverFlow = 1'b0;
	end
	endfunction
	
	function Even;					//返回是否为偶数
	input[31:0] A;
	integer i = 0;
	integer sum = 0;
	
	begin
		sum = 0;
		for(i = 0; i < 32; i = i + 1)
		begin
			sum = sum + A[i];
		end
		if(sum % 2 == 0)
			Even = 1;
		else
			Even = 0;
	end
	endfunction
	
	function [31:0] Left_Shift;
	input [31:0] A;
	input [4:0] B;
	reg [31:0] Out;
	integer i;
	
	begin
		Out = A;
		for(i = 0; i < 32; i = i + 1 )
		begin
			if(i < B)
			begin
				Out = {Out[30:0], Out[31]};
			end
			else
			begin
				i = 32;
			end
		end
		Left_Shift = Out;
	end
	endfunction
	
	function [31:0] Right_Shift;
	input [31:0] A;
	input [4:0] B;
	reg [31:0] Out;
	integer i;
	
	begin
		Out = A;
		for(i = 0; i < 32; i = i + 1 )
		begin
			if(i < B)
			begin
				Out = {Out[0], Out[31:1]};
			end
			else
			begin
				i = 32;
			end
		end
		Right_Shift = Out;
	end
	endfunction


	assign C =	(F == 2'b00) ? A + B :
					(F == 2'b01) ? A - B :
					(F == 2'b10) ? A | B : 0;
					//(F == 2'b11 && OverFlow(A, B) == 1) ? A :
					//(F == 2'b11 && OverFlow(A, B) == 0) ? A + B : 0;
					//(F == 2'b11 && Even(A)) ? Right_Shift(A, B[4:0]) : 
					//(F == 2'b11 && Even(B)) ? Left_Shift(A, B[4:0]) : 0;
endmodule
