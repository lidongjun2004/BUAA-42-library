`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:33:08 10/21/2021 
// Design Name: 
// Module Name:    BlockChecker 
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
`define S1 1	//b
`define S2 2	//e
`define S3 3	//g
`define S4 4	//i
`define S5 5	//n
`define S6 6	//e
`define S7 7	//n
`define S8 8	//d
`define S9 9	//wait for blank
module BlockChecker(
    input clk,
    input reset,
    input [7:0] in,
    output result
    );

	reg [32:0] cnt;
	reg [3:0] status;
	reg flag;
	
	initial
	begin
		cnt <= 1;
		status <= `S0;
		flag <= 1;
	end
	
	always @(reset == 1)
	begin
		status <= `S0;
		cnt <= 1;
		flag <= 1;
	end
	
	always @(posedge clk)
	begin
		case(status)
		
		`S0:
		begin
			if(in == "b" || in == "B")
				status <= `S1;
			else if(in == "e" || in == "E")
				status <= `S6;
			else if(in != " ")
				status <= `S9;
		end
		
		`S1:
		begin
			if(in == "e" || in == "E")
				status <= `S2;
			else
				status <= `S9;
		end
		
		`S2:
		begin
			if(in == "g" || in == "G")
				status <= `S3;
			else
				status <= `S9;
		end
		
		`S3:
		begin
			if(in == "i" || in == "I")
				status <= `S4;
			else
				status <= `S9;
		end
		
		`S4:
		begin
			if(in == "n" || in == "N")
			begin
				status <= `S5;
				if(flag == 1)
				begin
					cnt <= cnt + 1;
				end
			end
			else
			begin
				status <= `S9;
			end
		end
		
		`S5:
		begin
			if(in == " ")
			begin
				status <= `S0;
			end
			else
			begin
				status <= `S9;
				if(flag == 1)
				begin
					cnt <= cnt - 1;
				end
			end
		end
		
		`S6:
		begin
			if(in == "n" || in == "N")
				status <= `S7;
			else
				status <= `S9;
		end
		
		`S7:
		begin
			if(in == "d" || in == "D")
			begin
				status <= `S8;
				if(flag == 1)
				begin
					cnt <= cnt - 1;
				end
			end
			else
			begin
				status <= `S9;
			end
		end
		
		`S8:
		begin
			if(in == " ")
			begin
				status <= `S0;
				if(cnt == 0)
				begin
					flag = 0;
				end
			end
			else
			begin
				status <= `S9;
				if(flag == 1)
				begin
					cnt <= cnt + 1;
				end
			end
		end
		
		`S9:
		begin
			if(in == " ")
			begin
				status <= `S0;
			end
		end
		endcase
	end
	
	assign result = (cnt == 1) ? 1 : 0;
endmodule
