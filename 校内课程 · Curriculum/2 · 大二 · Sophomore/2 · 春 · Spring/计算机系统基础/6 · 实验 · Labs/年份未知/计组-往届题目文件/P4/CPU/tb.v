`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   17:29:26 11/19/2021
// Design Name:   BuildnPC
// Module Name:   E:/.main/CO/P4/CPU/tb.v
// Project Name:  CPU
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: BuildnPC
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
	reg [31:0] PC;
	reg [31:0] RegData;
	reg [31:0] Instr;
	reg [31:0] ALURes;
	reg [1:0] nPCctr;

	// Outputs
	wire [31:0] nPC;

	// Instantiate the Unit Under Test (UUT)
	BuildnPC uut (
		.PC(PC), 
		.RegData(RegData), 
		.Instr(Instr), 
		.ALURes(ALURes), 
		.nPCctr(nPCctr), 
		.nPC(nPC)
	);

	initial begin
		// Initialize Inputs
		PC = 16'h3000;
		RegData = 100;
		Instr = 200;
		ALURes = 1;
		nPCctr = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here

	end
      
endmodule

