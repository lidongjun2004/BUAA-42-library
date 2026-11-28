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
	 input [31:0] instr,
    output reg RegDst,
    output reg ALUSrc,
    output reg MemtoReg,
    output reg RegWrite,
    output reg MemWrite,
    output reg nPC_sel,
    output reg [1:0] ExtOp,
    output reg [3:0] ALUctr,
    output reg SavePC,
	 output reg [1:0] MemAddrctr,
    output reg [2:0] nPCctr,
	 output reg [1:0] Tnew,
	 output reg [1:0] Tuse,
	 output reg Lui,
	 output reg ALUSign,
	 output reg MemExtOp,
	 output reg [2:0] BCtr,
	 output reg [2:0] MDCtr,
	 output reg MD,
	 output reg ShiftImm,
	 output reg [1:0] SavePCCtr
    );

	wire lb;
	wire lbu;
	wire lh;
	wire lhu;
	wire lw;
	wire sb;
	wire sh;
	wire sw;
	wire add;
	wire addu;
	wire sub;
	wire subu;
	wire mult;
	wire multu;
	wire div;
	wire divu;
	wire sll;
	wire srl;
	wire sra;
	wire sllv;
	wire srlv;
	wire srav;
	wire _and;
	wire _or;
	wire _xor;
	wire _nor;
	wire addi;
	wire addiu;
	wire andi;
	wire ori;
	wire xori;
	wire lui;
	wire slt;
	wire slti;
	wire sltiu;
	wire sltu;
	wire beq;
	wire bne;
	wire blez;
	wire bgtz;
	wire bltz;
	wire bgez;
	wire j;
	wire jal;
	wire jalr;
	wire jr;
	wire mfhi;
	wire mflo;
	wire mthi;
	wire mtlo;
	
	initial
	begin
			RegDst 		<= 0;
			ALUSrc 		<= 0;
			MemtoReg 	<= 0;
			RegWrite 	<= 0;
			MemWrite 	<= 0;
			nPC_sel		<= 0;
			ExtOp			<= 2'b00;
			ALUctr		<= 4'b0000;
			SavePC		<= 0;
			nPCctr		<= 3'b00;
			Tnew			<= 2'b00;
			Tuse			<= 2'b00;
			Lui			<= 1'b0;
			MemAddrctr	<= 2'b00;
			ALUSign		<= 1'b0;
			MemExtOp		<= 1'b0;
			BCtr			<= 3'b0;
			MD				<= 1'b0;
			ShiftImm		<= 1'b0;
			SavePCCtr	<= 2'b00;
	end
	
	assign lb		= (opcode == 6'b100000) ? 1 : 0;
	assign lbu		= (opcode == 6'b100100) ? 1 : 0;
	assign lh		= (opcode == 6'b100001) ? 1 : 0;
	assign lhu		= (opcode == 6'b100101) ? 1 : 0;
	assign lw		= (opcode == 6'b100011) ? 1 : 0;
	assign sb		= (opcode == 6'b101000) ? 1 : 0;
	assign sh		= (opcode == 6'b101001) ? 1 : 0;
	assign sw		= (opcode == 6'b101011) ? 1 : 0;
	assign add		= (opcode == 6'b000000 && func == 6'b100000) ? 1 : 0;
	assign addu		= (opcode == 6'b000000 && func == 6'b100001) ? 1 : 0;
	assign sub		= (opcode == 6'b000000 && func == 6'b100010) ? 1 : 0;
	assign subu		= (opcode == 6'b000000 && func == 6'b100011) ? 1 : 0;
	assign mult		= (opcode == 6'b000000 && func == 6'b011000) ? 1 : 0;
	assign multu	= (opcode == 6'b000000 && func == 6'b011001) ? 1 : 0;
	assign div		= (opcode == 6'b000000 && func == 6'b011010) ? 1 : 0;
	assign divu		= (opcode == 6'b000000 && func == 6'b011011) ? 1 : 0;
	assign sll		= (opcode == 6'b000000 && func == 6'b000000) ? 1 : 0;
	assign srl		= (opcode == 6'b000000 && func == 6'b000010) ? 1 : 0;
	assign sra		= (opcode == 6'b000000 && func == 6'b000011) ? 1 : 0;
	assign sllv		= (opcode == 6'b000000 && func == 6'b000100) ? 1 : 0;
	assign srlv		= (opcode == 6'b000000 && func == 6'b000110) ? 1 : 0;
	assign srav		= (opcode == 6'b000000 && func == 6'b000111) ? 1 : 0;
	assign _and		= (opcode == 6'b000000 && func == 6'b100100) ? 1 : 0;
	assign _or		= (opcode == 6'b000000 && func == 6'b100101) ? 1 : 0;
	assign _xor		= (opcode == 6'b000000 && func == 6'b100110) ? 1 : 0;
	assign _nor		= (opcode == 6'b000000 && func == 6'b100111) ? 1 : 0;
	assign addi		= (opcode == 6'b001000) ? 1 : 0;
	assign addiu	= (opcode == 6'b001001) ? 1 : 0;
	assign andi		= (opcode == 6'b001100) ? 1 : 0;
	assign ori		= (opcode == 6'b001101) ? 1 : 0;
	assign xori		= (opcode == 6'b001110) ? 1 : 0;
	assign lui		= (opcode == 6'b001111) ? 1 : 0;
	assign slt		= (opcode == 6'b000000 && func == 6'b101010) ? 1 : 0;
	assign slti		= (opcode == 6'b001010) ? 1 : 0;
	assign sltiu	= (opcode == 6'b001011) ? 1 : 0;
	assign sltu		= (opcode == 6'b000000 && func == 6'b101011) ? 1 : 0;
	assign beq		= (opcode == 6'b000100) ? 1 : 0;
	assign bne		= (opcode == 6'b000101) ? 1 : 0;
	assign blez		= (opcode == 6'b000110) ? 1 : 0;
	assign bgtz		= (opcode == 6'b000111) ? 1 : 0;
	assign bltz		= (opcode == 6'b000001 && instr[20:16] == 5'b00000) ? 1 : 0;
	assign bgez		= (opcode == 6'b000001 && instr[20:16] == 5'b00001) ? 1 : 0;
	assign j			= (opcode == 6'b000010) ? 1 : 0;
	assign jal		= (opcode == 6'b000011) ? 1 : 0;
	assign jalr		= (opcode == 6'b000000 && func == 6'b001001) ? 1 : 0;
	assign jr		= (opcode == 6'b000000 && func == 6'b001000) ? 1 : 0;
	assign mfhi		= (opcode == 6'b000000 && func == 6'b010000) ? 1 : 0;
	assign mflo		= (opcode == 6'b000000 && func == 6'b010010) ? 1 : 0;
	assign mthi		= (opcode == 6'b000000 && func == 6'b010001) ? 1 : 0;
	assign mtlo		= (opcode == 6'b000000 && func == 6'b010011) ? 1 : 0;
	
	//Tnew为流水线寄存器更新时间,Tuse为第一次使用寄存器值时间
	//为防止冲突，跳转类等指令若无需使用Tuse和Tnew则Tuse = 2'b11,Tnew = 2'b00
	//在GRF处产生数据Tnew=2'b01，在ALU处产生数据Tnew=2'b10，在DM处产生数据Tnew=2'b11
	//在GRF处使用数据Tsue=2'b00，在ALU处使用数据Tuse=2'b01，在DM处使用数据Tuse=2'b10
	always@(*)
	begin
		ALUSrc <= (lb||lbu||lh||lhu||lw||sb||sh||sw||addi||addiu||andi||ori||xori||lui||slti||sltiu) ? 1 : 0;
		MemtoReg <= (lb||lbu||lh||lhu||lw) ? 1 : 0;
		RegWrite <= (sb||sh||sw||mult||multu||div||divu||beq||bne||blez||bgtz||bgez||bltz||j||jr||mthi||mtlo) ? 0 : 1;
		MemWrite <= (sb||sh||sw) ? 1 : 0;
		nPC_sel <= (beq||bne||blez||bltz||bgez||bgtz||j||jal||jr||jalr) ? 1 : 0;
		ExtOp <= (lb||lbu||lh||lhu||lw||sb||sh||sw||addiu||addi||slti||sltiu) ? 2'b01 : 
					(lui) ? 2'b10 : 2'b00;
		ALUctr <=	(sub||subu) ? 4'b0001 : 
						(ori||_or) ? 4'b0010 :
						(_and||andi) ? 4'b0011 : 
						(_xor||xori) ? 4'b0100 : 
						(_nor) ? 4'b0101 : 
						(sll||sllv) ? 4'b0110 :
						(srl||srlv) ? 4'b0111 : 
						(sra||srav) ? 4'b1000 :
						(slt||sltu||slti||sltiu) ? 4'b1001 : 4'b0000;
		SavePC <= (jal||jalr) ? 1 : 0;
		SavePCCtr <=	(jal) ? 2'b00 : 
							(jalr) ? 2'b01 : 2'b00;
		nPCctr <=	(beq||bne||blez||bltz||bgez||bgtz) ? 3'b000 : 
						(jal) ? 3'b001 : 
						(jr||jalr) ? 3'b010 :
						(j) ? 3'b011 : 3'b000;
		Tnew <=	(lui||jal||jalr) ? 2'b01 :
					(add||addu||sub||subu||mult||multu||div||divu||sll||srl||sra||sllv||srlv||srav||_and||_or||_xor||_nor||addi||addiu||andi||ori||xori||slt||sltu||slti||sltiu||mfhi||mflo||mthi||mtlo) ? 2'b10 : 
					(lw||sw||lh||lhu||sh||lb||lbu||sb) ? 2'b11 : 2'b11;
		Tuse <=	(jr||jalr||beq||bne||bgtz||bgez||bltz||blez) ? 2'b00 : 
					(add||addu||sub||subu||mult||multu||div||divu||sll||srl||sra||sllv||srlv||srav||_and||_or||_xor||_nor||addi||addiu||andi||ori||xori||slt||sltu||slti||sltiu||mthi||mtlo||sw||sh||sb||lw||lh||lb||lhu||lbu) ? 2'b01 :
					(lui||j||jal) ? 2'b11 : 2'b00;
		Lui <= (lui) ? 1'b1 : 1'b0;
		MemAddrctr <=	(lw||sw) ? 2'b00 : 
							(lh||sh||lhu) ? 2'b01 : 
							(lb||sb||lbu) ? 2'b10 : 2'b00;
		ALUSign <= (addu||subu||multu||divu||addiu||sltiu||sltu) ? 1'b0 : 1'b1;
		MemExtOp <= (lw||lh||lb) ? 1'b0 : 1'b1;
		BCtr		<= (beq) ? 3'b000 : 
						(bne) ? 3'b001 :
						(blez) ? 3'b010 :
						(bltz) ? 3'b011 :
						(bgez) ? 3'b100 :
						(bgtz) ? 3'b101 : 3'b000;
		MDCtr		<= (mult) ? 3'b000 : 
						(multu) ? 3'b001 :
						(div) ? 3'b010 :
						(divu) ? 3'b011 :
						(mflo) ? 3'b100 :
						(mfhi) ? 3'b101 :
						(mtlo) ? 3'b110 :
						(mthi) ? 3'b111 : 3'b000;
		MD			<= (mult||multu||div||divu||mfhi||mflo||mthi||mtlo) ? 1'b1 : 1'b0;
		ShiftImm	<= (sll||srl||sra) ? 1'b1 : 1'b0;
	end
endmodule
