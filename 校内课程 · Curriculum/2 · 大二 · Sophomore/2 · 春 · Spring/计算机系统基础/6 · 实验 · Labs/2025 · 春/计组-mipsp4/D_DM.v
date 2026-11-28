`timescale 1ns / 1ps
`default_nettype none
module D_DM(
    input wire clk,
    input wire reset,
	input wire [31:0] pc,
    input wire memoryReadEnable,
    input wire memoryWriteEnable,
    input wire [31:0] memoryAddress,
    input wire [31:0] memoryWriteData,
    output reg [31:0] memoryReadData
    );
	/*
	 * 0x0000 ~ 0x2FFF
	 * totally 0x3000 bytes as 0xc00 ints
	 * that is, 3072 ints
	 */
	reg[31:0] data[0:3071];
	integer i;
	initial begin
		for(i=0;i<3072;i=i+1) data[i] = 0;
	end
	always @(*) begin
		if(memoryReadEnable) begin
			if(memoryAddress[1:0]!=0||memoryAddress>32'h2fff) begin
				memoryReadData = 32'hXXXXXXXX;
			end else begin
				memoryReadData = data[memoryAddress>>2];
			end
		end else begin
			memoryReadData = 32'hZZZZZZZZ;
		end
	end
	always @(posedge clk) begin
		if(reset) begin
			for(i=0;i<3072;i=i+1) data[i] <= 0;
		end else begin
			if(memoryReadEnable) begin
				if(memoryAddress[1:0]!=0||memoryAddress>32'h2fff)
					$display("bad memoryAddress read %h at pc %h\n",memoryAddress,pc);
			end
			if(memoryWriteEnable) begin
				if(memoryAddress[1:0]!=0||memoryAddress>32'h2fff) begin
					$display("bad memoryAddress write *%h <= %h\n",memoryAddress, memoryWriteData);
				end else begin
					data[memoryAddress>>2] <= memoryWriteData;
					$display("@%h: *%h <= %h", pc, memoryAddress, memoryWriteData);
				end
			end
		end
	end
endmodule
