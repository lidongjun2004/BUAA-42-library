`timescale 1ns / 1ps
`default_nettype none
module B_Decoder(
    input wire [31:0] pc,
    input wire [31:0] opcode,
	output wire [5:0] op6,
	output wire [4:0] rs5,
	output wire [4:0] rt5,
	output wire [4:0] rd5,
	output wire [4:0] shamt5,
	output wire [5:0] funct6,
	output wire [15:0] imm16,
	output wire [25:0] jmm26,
	output wire [31:0] zeroimm,
	output wire [31:0] signimm
    );
	assign op6=opcode[31:26];
	assign rs5=opcode[25:21];
	assign rt5=opcode[20:16];
	assign rd5=opcode[15:11];
	assign shamt5=opcode[10:6];
	assign funct6=opcode[5:0];
	assign imm16=opcode[15:0];
	assign jmm26=opcode[25:0];
	assign zeroimm={{16{1'b0}},imm16};
	assign signimm={{16{imm16[15]}},imm16};
endmodule
