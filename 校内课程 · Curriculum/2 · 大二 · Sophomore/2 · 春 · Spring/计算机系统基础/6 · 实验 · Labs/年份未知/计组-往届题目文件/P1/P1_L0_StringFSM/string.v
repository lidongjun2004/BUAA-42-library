`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:49:24 10/21/2021 
// Design Name: 
// Module Name:    string 
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
`define S0 0	//reset
`define S1 1	//wrong
`define S2 2	//num
`define S3 3	//num + op
module string(
    input clk,
    input clr,
    input [7:0] in,
    output out
    );
	 
	reg [1:0] status;
	
	function is_num;
		input [7:0] char;

		is_num = ("0" <= char && char <= "9") ? 1 : 0;
	endfunction
	
	function is_op;
		input [7:0] char;
		
		is_op = (char == "+" || char == "*") ? 1 : 0;
	endfunction
	
	initial
	begin
		status <= `S0;
	end
	
	always @(posedge clr)
	begin
		status <= `S0;
	end
	
	always @(posedge clk)
	begin
		case(status)
		`S0:
		begin
			if(is_num(in))
			begin
				status <= `S2;
			end
			else
			begin
				status <= `S1;
			end
		end
		`S2:
		begin
			if(is_op(in))
			begin
				status <= `S3;
			end
			else
			begin
				status <= `S1;
			end
		end
		`S3:
		begin
			if(is_num(in))
			begin
				status <= `S2;
			end
			else
			begin
				status <= `S1;
			end
		end
		endcase
	end
	
assign out = (status == `S2) ? 1 : 0;
endmodule
