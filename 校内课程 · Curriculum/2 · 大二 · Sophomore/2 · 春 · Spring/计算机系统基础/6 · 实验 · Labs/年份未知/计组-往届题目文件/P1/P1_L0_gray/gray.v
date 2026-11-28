`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:40:29 10/21/2021 
// Design Name: 
// Module Name:    gray 
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
module gray(
    input Clk,
    input Reset,
    input En,
    output [2:0] Output,
    output Overflow
    );
	 
	 reg [2:0] cnt;
	 reg isoverflow;
	 
	 function [2:0] Gray;
		input [2:0] num;
		begin
			Gray[0] = num[1] ^ num[0];
			Gray[1] = num[2] ^ num[1];
			Gray[2] = num[2];
		end
	 endfunction
	 
	 initial
	 begin
		cnt <= 0;
		isoverflow <= 0;
	 end
	 
	 always @(posedge Clk)
	 begin
		if(Reset)
		begin
			cnt <= 0;
			isoverflow <= 0;
		end
		else if(En)
		begin
			if(cnt == 7)
			begin
				isoverflow <= 1;
				cnt <= 0;
			end
			else
			begin
				cnt <= cnt + 1;
			end
		end
	 end
	 
	 assign Output = Gray(cnt);
	 assign Overflow = isoverflow;
endmodule
