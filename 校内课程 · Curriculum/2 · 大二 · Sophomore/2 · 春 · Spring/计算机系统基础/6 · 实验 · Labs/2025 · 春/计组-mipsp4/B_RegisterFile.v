`timescale 1ns / 1ps
`default_nettype none
module B_RegisterFile(
    input wire clk,
    input wire reset,
	input wire [31:0] pc,
    input wire [4:0] read1Address,
    input wire [4:0] read2Address,
    input wire writeEnable,
    input wire [4:0] writeAddress,
    input wire [31:0] writeData,
    output reg [31:0] read1Data,
    output reg [31:0] read2Data
    );
	/*
	 * Register $0 ~ $31.
	 * Note that $0 will never be written.
	 */
	reg[31:0] data[0:31];
	integer i;
	initial begin
		for(i=0;i<=31;i=i+1) data[i]=0;
	end
	always @(*) begin
		read1Data = data[read1Address];
		read2Data = data[read2Address];
	end
	always @(posedge clk) begin
		if(reset) begin
			for(i=0;i<=31;i=i+1) data[i]=0;
		end else begin
			if(writeEnable) begin
				if(writeAddress==0) begin
				
				end else begin
					$display("@%h: $%d <= %h", pc, writeAddress, writeData);
					data[writeAddress] <= writeData;
				end
			end
		end
	end
endmodule
