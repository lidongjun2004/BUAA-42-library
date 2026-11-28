`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   10:06:45 10/21/2021
// Design Name:   string
// Module Name:   E:/.main/cscore/P1/P1_L0_StringFSM/string_tb.v
// Project Name:  P1_L0_StringFSM
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: string
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module string_tb;

	// Inputs
	reg clk;
	reg clr;
	reg [7:0] in;

	// Outputs
	wire out;

	// Instantiate the Unit Under Test (UUT)
	string uut (
		.clk(clk), 
		.clr(clr), 
		.in(in), 
		.out(out)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		clr = 1;
		in = 0;

		// Wait 100 ns for global reset to finish
		#1 clr = 0;
			in = "1";
		#2 in = "+";
		#2 in = "1";
			
        
		// Add stimulus here

	end
   
	always #1 clk = ~clk;
endmodule

