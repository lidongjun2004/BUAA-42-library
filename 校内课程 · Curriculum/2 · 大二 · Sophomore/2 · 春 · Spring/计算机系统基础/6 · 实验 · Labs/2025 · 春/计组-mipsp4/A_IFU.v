`timescale 1ns / 1ps
`default_nettype none
module A_IFU(
    input wire clk,
    input wire reset,
    input wire pcWriteEnable,
    input wire [31:0] pcWriteData,
    output reg [31:0] pc,
    output reg [31:0] opcode
    );
	/*
	 * 0x3000 ~ 0x7FFF
	 * totally 0x4000 bytes as 0x1000 ints
	 * that is, 4096 ints
	 */
	reg[31:0] data[0:4095];
	reg badPc;
	integer i;
	initial begin
		$readmemh("code.txt",data);
		pc = 32'h3000;
		opcode = data[0];
		badPc = 0;
	end
	always @(*) begin
		// pc - 0x3000
		badPc = 0;
		if((pc[1:0]!=0)||pc<32'h3000||pc>32'h7fff) begin
			// boom!
			opcode = 32'hXXXXXXXX;
			badPc = 1;
		end else begin
			opcode = data[(pc-32'h3000)>>2];
			if(opcode === 32'hXXXXXXXX) begin
				badPc = 1;
			end
		end
	end
	always @(posedge clk) begin
		if(reset) begin
			pc <= 32'h3000;
		end else begin
			if(badPc) begin
				// $display("bad pc @%h as opcode %h\n", pc, opcode);
				$finish;
			end
			if(pcWriteEnable)
				pc <= pcWriteData;
			else
				pc <= pc + 4;
		end
	end
endmodule
