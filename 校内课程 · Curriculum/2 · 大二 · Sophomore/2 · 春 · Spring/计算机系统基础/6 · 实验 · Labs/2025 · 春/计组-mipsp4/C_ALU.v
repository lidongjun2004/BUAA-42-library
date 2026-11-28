`timescale 1ns / 1ps
`default_nettype none
module C_ALU(
	input wire clk,
    input wire [31:0] pc,
    input wire [31:0] opcode,
    input wire [31:0] rsVal,
    input wire [31:0] rtVal,
    output reg regWriteEnable,
    output reg [4:0] regWriteId,
    output reg [31:0] regWriteData,
    output reg pcWriteEnable,
    output reg [31:0] pcWriteData,
    output reg [31:0] memoryAddress,
    output reg memoryReadEnable,
    input wire [31:0] memoryReadInputData,
    output reg memoryWriteEnable,
    output reg [31:0] memoryWriteOutputData
    );
	/*
	 * Decoder and ALU
	 * well, totally combinational.
	 * firstly, we need to decode.
	 */
	wire[5:0] op6; assign op6=opcode[31:26];
	wire[4:0] rs5; assign rs5=opcode[25:21];
	wire[4:0] rt5; assign rt5=opcode[20:16];
	wire[4:0] rd5; assign rd5=opcode[15:11];
	wire[4:0] shamt5; assign shamt5=opcode[10:6];
	wire[5:0] funct6; assign funct6=opcode[5:0];
	wire[15:0] imm16; assign imm16=opcode[15:0];
	wire[25:0] jmm26; assign jmm26=opcode[25:0];
	wire[31:0] zeroimm; assign zeroimm={{16{1'b0}},imm16};
	wire[31:0] signimm; assign signimm={{16{imm16[15]}},imm16};
	wire[31:0] address; assign address=rsVal+signimm;
	wire[31:0] bta; assign bta=pc+32'd4+(signimm<<2);
	wire[31:0] jta; assign jta=((pc+32'd4)&32'hf0000000)|{4'b0000,jmm26[25:0],2'b00};
	wire[31:0] bad; assign bad=32'hZZZZZZZZ;
	
	reg badOpcode;
	always @(*) begin
		regWriteEnable = 0; regWriteId = bad; regWriteData = bad;
		pcWriteEnable = 0; pcWriteData = bad;
		memoryAddress = bad; memoryReadEnable = 0;
		memoryWriteEnable = 0; memoryWriteOutputData = bad;
		badOpcode = 0;
		if(opcode == 0) begin
			// [$0] = [$0] << 0
		end else if(op6 == 0 && funct6 == 32) begin
			// GPR[rd] <= GPR[rs] + GPR[rt]
			regWriteEnable = 1;
			regWriteId = rd5;
			regWriteData = rsVal + rtVal;
		end else if(op6 == 0 && funct6 == 34) begin
			// GPR[rd] <= GPR[rs] - GPR[rt]
			regWriteEnable = 1;
			regWriteId = rd5;
			regWriteData = rsVal - rtVal;
		end else if(op6 == 13) begin
			// [rt] = [rs] | zeroimm
			regWriteEnable = 1;
			regWriteId = rt5;
			regWriteData = rsVal | zeroimm;
		end else if(op6 == 15) begin
			// [rt] = {imm, 16'b0}
			regWriteEnable = 1;
			regWriteId = rt5;
			regWriteData = zeroimm << 16;
		end else if(op6 == 4) begin
			// if([rs] == [rt]) pc = bta;
			pcWriteData = bta;
			pcWriteEnable = (rsVal == rtVal);
		end else if(op6 == 3) begin
			// $ra = pc + 4, pc = jta
			regWriteEnable = 1;
			regWriteId = 31;
			regWriteData = pc + 4;
			pcWriteEnable = 1;
			pcWriteData = jta;
		end else if(op6 == 0 && funct6 == 8) begin
			// pc = [rs]
			pcWriteEnable = 1;
			pcWriteData = rsVal;
		end else if(op6 == 35) begin
			// [rt] = [address]
			regWriteEnable = 1;
			regWriteId = rt5;
			regWriteData = memoryReadInputData;
			memoryReadEnable = 1;
			memoryAddress = address;
		end else if(op6 == 43) begin
			// [address] = [rt]
			memoryWriteEnable = 1;
			memoryAddress = address;
			memoryWriteOutputData = rtVal;
		end else begin
			// totally bad.
			badOpcode = 1;
		end
	end
	always @(posedge clk) begin
		if(badOpcode) begin
			// $display("unknown opcode @%h(0x%h): op6=%d, funct6=%d\n",pc,opcode,op6,funct6);
		end
	end
endmodule
