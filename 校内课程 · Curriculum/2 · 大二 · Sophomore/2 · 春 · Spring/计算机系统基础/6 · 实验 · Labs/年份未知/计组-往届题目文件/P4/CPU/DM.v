`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:22:47 11/18/2021 
// Design Name: 
// Module Name:    DM 
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
module BuildDM(
    input clk,
    input reset,
	 input MemWrite,
    input [9:0] Addr,
	 input [31:0] ALURes,
	 input [31:0] PC,
    input [31:0] DataIn,
    output [31:0] DataOut
    );

	reg [31:0] DM [1023:0];
	integer i;
	
	always @(posedge clk)
	begin
		if(reset == 1)
		begin
			for(i = 0; i < 1024; i = i + 1)
			begin
				DM[i] <= 32'h0;
			end
		end
		else if(MemWrite == 1)
		begin
			DM[Addr] <= DataIn;
			$display("@%h: *%h <= %h", PC, ALURes, DataIn);
		end
	end
	
	assign DataOut = DM[Addr];
endmodule
