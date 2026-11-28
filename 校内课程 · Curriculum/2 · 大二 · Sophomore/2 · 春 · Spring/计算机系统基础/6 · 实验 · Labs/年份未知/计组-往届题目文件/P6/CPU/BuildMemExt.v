`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:16:45 12/16/2021 
// Design Name: 
// Module Name:    BuildMemExt 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module BuildMemExt(
    input [31:0] Addr,
    input [31:0] MemData,
    input MemExtOp,
    input [1:0] MemAddrCtr,
    output [31:0] MemExtData
    );
	 
	function [31:0] sign_ext16;
	input [15:0] A;
	
	begin
		if(A[15] == 1'b0)
			sign_ext16 = {16'h0000, A};
		else if(A[15] == 1'b1)
			sign_ext16 = {16'hffff, A};
	end
	endfunction
	
	function [31:0] zero_ext16;
	input [15:0] A;
	
	begin
		zero_ext16 = {16'h0000, A};
	end
	endfunction
	
	function [31:0] sign_ext8;
	input [7:0] A;
	
	begin
		if(A[7] == 1'b0)
			sign_ext8 = {24'h000000, A};
		else if(A[7] == 1'b1)
			sign_ext8 = {24'hffffff, A};
	end
	endfunction
	
	function [31:0] zero_ext8;
	input [7:0] A;
	
	begin
		zero_ext8 = {16'h000000, A};
	end
	endfunction
	
	assign MemExtData =	(MemExtOp == 1'b0) ? 
								((MemAddrCtr == 2'b00) ? MemData : 
								(MemAddrCtr == 2'b01 && Addr[1] == 1'b0) ? sign_ext16(MemData[15:0]) : 
								(MemAddrCtr == 2'b01 && Addr[1] == 1'b1) ? sign_ext16(MemData[31:16]) : 
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b00) ? sign_ext8(MemData[7:0]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b01) ? sign_ext8(MemData[15:8]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b10) ? sign_ext8(MemData[23:16]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b11) ? sign_ext8(MemData[31:24]) : 32'b0) : 
								((MemAddrCtr == 2'b00) ? MemData : 
								(MemAddrCtr == 2'b01 && Addr[1] == 1'b0) ? zero_ext16(MemData[15:0]) : 
								(MemAddrCtr == 2'b01 && Addr[1] == 1'b1) ? zero_ext16(MemData[31:16]) : 
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b00) ? zero_ext8(MemData[7:0]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b01) ? zero_ext8(MemData[15:8]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b10) ? zero_ext8(MemData[23:16]) :
								(MemAddrCtr == 2'b10 && Addr[1:0] == 2'b11) ? zero_ext8(MemData[31:24]) : 32'b0);
endmodule
