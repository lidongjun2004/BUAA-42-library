`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:15:30 10/21/2021
// Design Name:   BlockChecker
// Module Name:   E:/.main/cscore/P1/P1_L1_BlockChecker/tb.v
// Project Name:  P1_L1_BlockChecker
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: BlockChecker
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module tb;

	// Inputs
	reg clk;
	reg reset;
	reg [7:0] in;

	// Outputs
	wire result;

	// Instantiate the Unit Under Test (UUT)
	BlockChecker uut (
		.clk(clk), 
		.reset(reset), 
		.in(in), 
		.result(result)
	);

	integer i;
	reg [0:32] test;
	
	initial begin
		// Initialize Inputs
		clk = 0;
		reset = 1;
		in = 0;
		i = 0;
		
		
		#2 in = " ";
		#2 in = " ";
		#2 in = "e";
		reset = 0;
		#2 in = "n";
		#2 in = "d";
		#2 in = "i";
		#2 in = "n";
		#2 in = "g";
		#2 in = "s";
		#2 in = " ";
		#2 in = "b";
		#2 in = "E";
		#2 in = "g";
		#2 in = "I";
		#2 in = "n";
		#2 in = " ";
		#2 in = " ";
		#2 in = "E";
		#2 in = "n";
		#2 in = "D";
		#2 in = " ";
		#2 in = " ";
		#2 in = "B";
		#2 in = "E";
		#2 in = "G";
		#2 in = "I";
		#2 in = "N";
		#2 in = "I";
		#2 in = "n";
		#2 in = "g";
		#2 in = " ";
		#2 in = "b";
		#2 in = "E";
		#2 in = "g";
		#2 in = "I";
		#2 in = "N";
		#2 in = " ";
		#2 in = "e";
		#2 in = "n";
		#2 in = "d";
		#2 in = " ";
		#2 in = "b";
		#2 in = "e";
		#2 in = "n";
		#2 in = "d";
		#2 in = " ";
		#2 in = " ";
		#2 in = "e";
		#2 in = "n";
		#2 in = "d";
		#2 in = " ";
		#2 in = "b";
		#2 in = "e";
		#2 in = "g";
		#2 in = "i";
		#2 in = "n";
		#2 in = " ";
		#2 in = "e";
		#2 in = "n";
		#2 in = "d";
		#2 in = " ";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		#2 in = "";
		
		// Wait 100 ns for global reset to finish
        
		// Add stimulus here

	end
	
	always #1 clk = ~clk;
endmodule

