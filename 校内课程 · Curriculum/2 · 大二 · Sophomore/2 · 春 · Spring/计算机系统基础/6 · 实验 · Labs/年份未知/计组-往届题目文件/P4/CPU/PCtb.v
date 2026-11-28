`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   11:07:32 11/18/2021
// Design Name:   PC
// Module Name:   E:/.main/Coding Document/Verilog/CPU/PCtb.v
// Project Name:  CPU
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: PC
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module PCtb;

	// Inputs
	reg clk;
	reg reset;
	reg nPC_sel;
	reg [31:0] nPC;

	// Outputs
	wire [31:0] PC;

	// Instantiate the Unit Under Test (UUT)
	PC uut (
		.clk(clk), 
		.reset(reset), 
		.nPC_sel(nPC_sel), 
		.nPC(nPC), 
		.PC(PC)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		reset = 0;
		nPC_sel = 0;
		nPC = 0;

		// Wait 100 ns for global reset to finish
		#6 nPC_sel = 1;
			nPC = 32'h3000;
      #2 nPC_sel = 0;
		// Add stimulus here

	end
	
	always #1 clk = ~clk;
      
endmodule

