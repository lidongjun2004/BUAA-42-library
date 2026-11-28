`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:01:21 11/18/2021 
// Design Name: 
// Module Name:    Controller 
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

module BuildController(
    input [5:0] opcode,
    input [5:0] func,
    output reg RegDst,
    output reg ALUSrc,
    output reg MemtoReg,
    output reg RegWrite,
    output reg MemWrite,
    output reg nPC_sel,
    output reg [1:0] ExtOp,
    output reg [1:0] ALUctr,
    output reg SavePC,
    output reg [1:0] nPCctr
    );

	reg [3:0] op;
	localparam nop = 0;
	localparam addu = 1;
	localparam subu = 2;
	localparam ori = 3;
	localparam lw = 4;
	localparam sw = 5;
	localparam beq = 6;
	localparam lui = 7;
	localparam jal = 8;
	localparam jr = 9;
	
	initial
	begin
		op <= nop;
	end
	
	always@(*)
	begin
		//addu
		if(opcode == 6'b000000 && func == 6'b100001)
		begin
			RegDst <= 1;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b00;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//subu
		else if(opcode == 6'b000000 && func == 6'b100011)
		begin
			RegDst <= 1;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b00;
			ALUctr <= 2'b01;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//ori
		else if(opcode == 6'b001101)
		begin
			RegDst <= 0;
			ALUSrc <= 1;
			MemtoReg <= 0;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b00;
			ALUctr <= 2'b10;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//lw
		else if(opcode == 6'b100011)
		begin
			RegDst <= 0;
			ALUSrc <= 1;
			MemtoReg <= 1;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b01;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//sw
		else if(opcode == 6'b101011)
		begin
			RegDst <= 0;
			ALUSrc <= 1;
			MemtoReg <= 0;
			RegWrite <= 0;
			MemWrite <= 1;
			nPC_sel <= 0;
			ExtOp <= 2'b01;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//beq
		else if(opcode == 6'b000100)
		begin
			RegDst <= 0;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 0;
			MemWrite <= 0;
			nPC_sel <= 1;
			ExtOp <= 2'b00;
			ALUctr <= 2'b01;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//lui
		else if(opcode == 6'b001111)
		begin
			RegDst <= 0;
			ALUSrc <= 1;
			MemtoReg <= 0;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b10;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
		//jal
		else if(opcode == 6'b000011)
		begin
			RegDst <= 0;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 1;
			MemWrite <= 0;
			nPC_sel <= 1;
			ExtOp <= 2'b00;
			ALUctr <= 2'b00;
			SavePC <= 1;
			nPCctr <= 2'b01;
		end
		//jr
		else if(opcode == 6'b000000 && func == 6'b0001000)
		begin
			RegDst <= 0;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 0;
			MemWrite <= 0;
			nPC_sel <= 1;
			ExtOp <= 2'b00;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b10;
		end
		else
		begin
			RegDst <= 0;
			ALUSrc <= 0;
			MemtoReg <= 0;
			RegWrite <= 0;
			MemWrite <= 0;
			nPC_sel <= 0;
			ExtOp <= 2'b00;
			ALUctr <= 2'b00;
			SavePC <= 0;
			nPCctr <= 2'b00;
		end
	end
endmodule
