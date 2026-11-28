`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   19:51:45 11/18/2021
// Design Name:   DM
// Module Name:   E:/.main/Coding Document/Verilog/CPU/DMtb.v
// Project Name:  CPU
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: DM
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module DMtb;

	// Inputs
	reg clk;
	reg reset;
	reg MemWrite;
	reg [4:0] Addr;
	reg [31:0] DataIn;

	// Outputs
	wire [31:0] DataOut;

	// Instantiate the Unit Under Test (UUT)
	DM uut (
		.clk(clk), 
		.reset(reset), 
		.MemWrite(MemWrite), 
		.Addr(Addr), 
		.DataIn(DataIn), 
		.DataOut(DataOut)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		reset = 0;
		MemWrite = 0;
		Addr = 0;
		DataIn = 0;

		// Wait 100 ns for global reset to finish
		#2	MemWrite = 1;
			DataIn = 1;
		#2 DataIn = 2;
        
		// Add stimulus here

	end
      
	always#1 clk = ~clk;
endmodule

