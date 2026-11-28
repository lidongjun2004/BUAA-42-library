`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:49:37 12/25/2021 
// Design Name: 
// Module Name:    CPU 
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
module BuildCPU(
	 input clk,
    input reset,
	 input interrupt,
	 input [5:0] HWInt,
	 input [1:0] interruptCtr,
    input [31:0] i_inst_rdata,
    input [31:0] m_data_rdata,
    output [31:0] i_inst_addr,
    output [31:0] m_data_addr,
    output [31:0] m_data_wdata,
    output [3 :0] m_data_byteen,
    output [31:0] m_inst_addr,
    output w_grf_we,
    output [4:0] w_grf_addr,
    output [31:0] w_grf_wdata,
    output [31:0] w_inst_addr,
	 output IRQ,
	 output MacroPC
    );

	//Stall
	wire Stall;
	
	//PC
	wire nPC_sel;
	wire [31:0] PC_nPC;
	wire [31:0] PC;
	
	//IM
	wire [31:0] Instr;
	
	//IFID
	wire [31:0] IFID_Instr_Out;
	wire [31:0] IFID_PC_Out;
	
	//Controller
	wire RegWrite;
	wire MemWrite;
	wire ALUSrc;
	wire SavePC;
	wire MemtoReg;
	wire [2:0] nPCctr;
	wire [3:0] ALUCtr;
	wire [1:0] ExtOp;
	wire Controller_nPC_sel;
	wire [1:0] Tnew;
	wire [1:0] Tuse;
	wire Lui;
	wire ALUSign;
	wire MemExtOp;
	wire [1:0] MemAddrCtr;
	wire [2:0] BCtr;
	wire [2:0] MDCtr;
	wire MD;
	wire ShiftImm;
	wire [1:0] SavePCCtr;
	wire CP0_Read;
	wire CP0_Write;
	wire Eret;
	
	//GRF
	wire [4:0] A1;
	wire [4:0] A2;
	wire [4:0] A3;
	wire [31:0] WriteData;
	wire [31:0] RD1;
	wire [31:0] RD2;
	
	//Cmp
	wire [31:0] Cmp1;
	wire [31:0] Cmp2;
	wire BAble;
	
	//EXT
	wire [31:0] Ext32;
	
	//nPC
	wire [31:0] nPC_RegData;
	
	//IDEX
	wire [4:0] IDEX_Addr_In;
	wire [4:0] IDEX_Addr_Out;
	wire [31:0] IDEX_Instr_In;
	wire [31:0] IDEX_PC_In;
	wire [31:0] IDEX_RD1_In;
	wire [31:0] IDEX_RD2_In;
	wire [31:0] IDEX_Imm_In;
	wire [31:0] IDEX_Instr_Out;
   wire [31:0] IDEX_PC_Out;
	wire [31:0] IDEX_RD1_Out;
	wire [31:0] IDEX_RD2_Out;
	wire [31:0] IDEX_Imm_Out;
	wire IDEX_RegWrite_In;
	wire IDEX_MemtoReg_In;
	wire IDEX_MemWrite_In;
	wire IDEX_SavePC_In;
	wire IDEX_ALUSrc_In;
	wire [3:0] IDEX_ALUCtr_In ;
	wire [1:0] IDEX_Tnew_In;
	wire IDEX_ALUSign_In;
	wire [1:0] IDEX_MemAddrCtr_In;
	wire [2:0] IDEX_MDCtr_In;
	wire IDEX_MD_In;
	wire IDEX_MemExtOp_In;
	wire IDEX_ShiftImm_In;
	wire IDEX_RegWrite_Out;
	wire IDEX_MemWrite_Out;
	wire IDEX_MemtoReg_Out;
	wire IDEX_SavePC_Out;
	wire IDEX_ALUSrc_Out;
	wire [3:0] IDEX_ALUCtr_Out;
	wire [1:0] IDEX_Tnew_Out;
	wire IDEX_Lui_Out;
	wire IDEX_Lui_In;
	wire IDEX_ALUSign_Out;
	wire [1:0] IDEX_MemAddrCtr_Out;
	wire IDEX_MemExtOp_Out;
	wire [2:0] IDEX_MDCtr_Out;
	wire IDEX_MD_Out;
	wire IDEX_ShiftImm_Out;
	
	//ALU
	wire [31:0] ALU1;
	wire [31:0] ALURes;
	wire [31:0] ALU2;
	
	//MD
	wire start;
	wire busy;
	wire [31:0] MDRes;
	
	//EXMEM
	wire [31:0] EXMEM_Instr_In;
   wire [31:0] EXMEM_PC_In;
	wire EXMEM_RegWrite_In;
	wire EXMEM_MemWrite_In;
	wire EXMEM_MemtoReg_In;
	wire EXMEM_SavePC_In;
	wire EXMEM_ALUSrc_In;
	wire [31:0] EXMEM_ALURes_In;
	wire [4:0] EXMEM_Addr_In;
	wire [1:0] EXMEM_Tnew_In;
   wire [31:0] EXMEM_Instr_Out;
   wire [31:0] EXMEM_PC_Out;
	wire EXMEM_RegWrite_Out;
	wire EXMEM_MemWrite_Out;
	wire EXMEM_MemtoReg_Out;
	wire EXMEM_SavePC_Out;
	wire EXMEM_ALUSrc_Out;
	wire [31:0] EXMEM_ALURes_Out;
	wire [4:0] EXMEM_Addr_Out;
	wire [1:0] EXMEM_Tnew_Out;
	wire [1:0] EXMEM_MemAddrCtr_Out;
	wire EXMEM_MemExtOp_Out;
	
	//DM
	wire [11:0] MemAddr;
	wire [31:0] MemIn;
	wire [31:0] MemOut;
	
	//BE
	wire [3:0] Byteen;

	//CP0
	wire [31:0] CP0_PC_In;
	wire [31:0] CP0_PC_Out;
	wire IntReq;
	wire [31:0] CP0_DataIn;
	wire [31:0] CP0_DataOut;
	wire delay;
	
	//MEMWB	
	wire [31:0] MEMWB_Instr_In;
   wire [31:0] MEMWB_PC_In;
	wire MEMWB_RegWrite_In;
	wire MEMWB_MemtoReg_In;
	wire MEMWB_SavePC_In;
	wire [31:0] MEMWB_MemData_In;
	wire [31:0] MEMWB_ALURes_In;
	wire [4:0] MEMWB_Addr_In;
	wire [1:0] MEMWB_Tnew_In;
   wire [31:0] MEMWB_Instr_Out;
   wire [31:0] MEMWB_PC_Out;
	wire MEMWB_RegWrite_Out;
	wire MEMWB_MemtoReg_Out;
	wire MEMWB_SavePC_Out;
	wire [31:0] MEMWB_MemData_Out;
	wire [31:0] MEMWB_ALURes_Out;
	wire [4:0] MEMWB_Addr_Out;
	wire [1:0] MEMWB_Tnew_Out;
	wire [31:0] EXMEM_RD2_In;
	wire [31:0] EXMEM_RD2_Out;

	
	// <------------ nPC <--
	//|                     |
	//PC -> IM -> IFID -> GRF -> IDEX -> ALU ->EXMEM -> DM -> MEMWB
	//CPU
	assign IRQ = IntReq;
	assign MacroPC =	($signed(MEMWB_Tnew_Out) > $signed(0)) ? MEMWB_PC_Out :
							($signed(EXMEM_Tnew_Out) > $signed(0)) ? EXMEM_PC_Out :	
							($signed(IDEX_Tnew_Out) > $signed(0)) ? IDEX_PC_Out : IFID_PC_Out;
	//PC				
	assign PC_nPC = (IntReq) ? 32'h4180 : nPC;
	BuildPC MyPC(																	
		.clk				(clk),														
		.reset			(reset),														
		.Stall			(Stall),
		.nPC_sel			(nPC_sel),													
		.nPC				(PC_nPC),														
		.PC				(PC));														
	//IM
	assign i_inst_addr = PC;
	//IFID
	assign IFID_reset =	(reset == 1) ? 1 : 
								(IntReq) ? 1 :
								(stall == 0 && Eret == 1) ? 1 : 0;//延迟槽清空,注意考虑暂停时的信号
	BuildIFID IFID(																	
		.clk				(clk),														
		.reset			(IFID_reset),												
		.InstrIn			(i_inst_rdata),	
		.Stall			(Stall),
		.PCIn				(PC),															
		.InstrOut		(IFID_Instr_Out),											
		.PCOut			(IFID_PC_Out));											
	BuildController	 MyController(												
		.opcode			(IFID_Instr_Out[31:26]), 								
		.func				(IFID_Instr_Out[5:0]),
		.instr			(IFID_Instr_Out),
		.RegDst			(), 															
		.ALUSrc			(ALUSrc),													
		.MemtoReg		(MemtoReg), 												
		.RegWrite		(RegWrite),													
		.MemWrite		(MemWrite),													
		.nPC_sel			(Controller_nPC_sel),									
		.ExtOp			(ExtOp),														
		.ALUctr			(ALUCtr),													
		.SavePC			(SavePC),													
		.nPCctr			(nPCctr),													
		.Tnew				(Tnew),
		.Tuse				(Tuse),
		.Lui				(Lui),
		.ALUSign			(ALUSign),
		.MemExtOp		(MemExtOp),
		.MemAddrctr		(MemAddrCtr),
		.BCtr				(BCtr),
		.MD				(MD),
		.MDCtr			(MDCtr),
		.ShiftImm		(ShiftImm),
		.SavePCCtr		(SavePCCtr),
		.CP0_Read		(CP0_Read),
		.CP0_Write		(CP0_Write),
		.Eret				(Eret));
	//暂停判断，若是IDEX或者EXMEM的指令来不及生成结果则暂停，GRF可以内部转发不考虑
	assign Stall =	(A1 != 5'b0 && IDEX_Addr_Out == A1 && $signed(Tuse) < $signed(IDEX_Tnew_Out)) ? 1 :
						(A1 != 5'b0 && EXMEM_Addr_Out == A1 && $signed(Tuse) < $signed(EXMEM_Tnew_Out)) ? 1 :
						(A2 != 5'b0 && ALUSrc == 0 && IDEX_Addr_Out == A2 && $signed(Tuse) < $signed(IDEX_Tnew_Out)) ? 1 :
						(A2 != 5'b0 && ALUSrc == 0 && EXMEM_Addr_Out == A2 && $signed(Tuse) < $signed(EXMEM_Tnew_Out)) ? 1 : 
						(busy == 1'b1 && MD == 1'b1) ? 1 : 
						(start == 1'b1 && MD == 1'b1) ? 1 : 0;
	//EXT
	BuildEXT MyEXT(																
		.Imm16			(IFID_Instr_Out[15:0]),									
		.ExtOp			(ExtOp),														
		.Ext32			(Ext32));													
	//GRF
	assign w_grf_we = MEMWB_RegWrite_Out;
	assign w_grf_addr = A3;
	assign w_grf_wdata = WriteData;
	assign w_inst_addr = MEMWB_PC_Out;
	assign A1 = IFID_Instr_Out[25:21];													
	assign A2 = IFID_Instr_Out[20:16];													
	assign A3 = MEMWB_Addr_Out;						
	assign WriteData =	(MEMWB_MemtoReg_Out == 1) ? MEMWB_MemData_Out :						
								(MEMWB_SavePC_Out == 1) ? MEMWB_PC_Out + 8 : MEMWB_ALURes_Out;				
	BuildGRF MyGRF(																	
		.clk				(clk),														
		.WE				(MEMWB_RegWrite_Out),									
		.reset			(reset),														
		.A1				(A1),															
		.A2				(A2),															
		.A3				(A3),															
		.PC				(MEMWB_PC_Out),											
		.WD				(WriteData),
		.Instr			(MEMWB_Instr_Out),
		.RD1				(RD1),														
		.RD2				(RD2));			
	//Cmp
	assign Cmp1 	=	(A1 != 5'b0 && A1 == IDEX_Addr_Out && IDEX_Tnew_Out == 0 && IDEX_SavePC_Out == 1) ? IDEX_PC_Out + 8 : 
							(A1 != 5'b0 && A1 == IDEX_Addr_Out && IDEX_Tnew_Out == 0 && IDEX_Lui_Out == 1) ? IDEX_Imm_Out :
							(A1 != 5'b0 && A1 == EXMEM_Addr_Out && EXMEM_SavePC_Out == 1) ? EXMEM_PC_Out + 8 :
							(A1 != 5'b0 && A1 == EXMEM_Addr_Out && EXMEM_MemtoReg_Out == 0) ? EXMEM_ALURes_Out :  RD1;
	assign Cmp2 	=	(A2 != 5'b0 && A2 == IDEX_Addr_Out && IDEX_Tnew_Out == 0 && IDEX_SavePC_Out == 1) ? IDEX_PC_Out + 8 : 
							(A2 != 5'b0 && A2 == IDEX_Addr_Out && IDEX_Tnew_Out == 0 && IDEX_Lui_Out == 1) ? IDEX_Imm_Out :
							(A2 != 5'b0 && A2 == EXMEM_Addr_Out && EXMEM_SavePC_Out == 1) ? EXMEM_PC_Out + 8 :
							(A2 != 5'b0 && A2 == EXMEM_Addr_Out && EXMEM_MemtoReg_Out == 0) ? EXMEM_ALURes_Out : RD2;
	BuildCmp MyCmp(
		.Cmp1				(Cmp1),
		.Cmp2				(Cmp2),
		.nPCCtr			(nPCctr),
		.BCtr				(BCtr),
		.nPCsel			(BAble)
		);
	assign nPC_sel 		=	(IntReq) ? 1 : 
									(Controller_nPC_sel == 1 && nPCctr == 3'b000 && !BAble) ? 0 : Controller_nPC_sel;
	assign nPC_RegData	=	Cmp1;
	BuildnPC MynPC(																
		.PC				(IFID_PC_Out),															
		.RegData			(nPC_RegData),														
		.Instr			(IFID_Instr_Out),														
		.nPCctr			(nPCctr),													
		.nPC				(nPC));														
	assign IDEX_Instr_In			=	(Stall == 1) ? 32'b0 : IFID_Instr_Out;
	assign IDEX_PC_In				=	(Stall == 1) ? 32'b0 : IFID_PC_Out;
	assign IDEX_SavePC_In		=	(Stall == 1) ? 1'b0 : SavePC;
	assign IDEX_RD1_In			=	(Stall == 1) ? 32'b0 : 
											(ShiftImm == 1'b1) ? {27'h0, IFID_Instr_Out[10:6]} : RD1;
	assign IDEX_RD2_In			=	(Stall == 1) ? 32'b0 : RD2;
	assign IDEX_Imm_In			=	(Stall == 1) ? 32'b0 : Ext32;
	assign IDEX_RegWrite_In		=	(Stall == 1) ? 1'b0 : RegWrite;
	assign IDEX_MemWrite_In		=	(Stall == 1) ? 1'b0 : MemWrite;
	assign IDEX_MemtoReg_In		=	(Stall == 1) ? 1'b0 : MemtoReg;
	assign IDEX_ALUSrc_In		=	(Stall == 1) ? 1'b0 : ALUSrc;
	assign IDEX_ALUCtr_In		=	(Stall == 1) ? 2'b0 : ALUCtr;
	assign IDEX_Tnew_In			=	(Stall == 1) ? 2'b0 : Tnew;
	assign IDEX_Lui_In 			=	(Stall == 1) ? 1'b0 : Lui;
	assign IDEX_ALUSign_In		=	(Stall == 1) ? 1'b0 : ALUSign;
	assign IDEX_MemExtOp_In		=	(Stall == 1) ? 1'b0 : MemExtOp;
	assign IDEX_MemAddrCtr_In	=	(Stall == 1) ? 2'b0 : MemAddrCtr;
	assign IDEX_MD_In				=	(Stall == 1) ? 1'b0 : MD;
	assign IDEX_MDCtr_In			=	(Stall == 1) ? 3'b0 : MDCtr;
	assign IDEX_CP0Write_In
	assign IDEX_CP0Read_In),
	assign IDEX_BJ_In),
	assign IDEX_ExcCode_In),
	assign IDEX_Addr_In			=	(Stall == 1) ? 5'b0 :  
											(RegWrite == 0) ? 5'b0 :
											(ALUSrc == 1) ? A2 : 
											(SavePC == 1 && SavePCCtr == 2'b00) ? 31 : IFID_Instr_Out[15:11];
	BuildIDEX IDEX(																
		.clk				(clk),													
		.reset			(reset),													
		.Instr_In		(IDEX_Instr_In),										
		.PC_In			(IDEX_PC_In),											
		.RD1_In			(IDEX_RD1_In),											
		.RD2_In			(IDEX_RD2_In),											
		.Imm_In			(IDEX_Imm_In),										
		.RegWrite_In	(IDEX_RegWrite_In),									
		.MemWrite_In	(IDEX_MemWrite_In),									
		.MemtoReg_In	(IDEX_MemtoReg_In),
		.SavePC_In		(IDEX_SavePC_In),
		.ALUSrc_In		(IDEX_ALUSrc_In),										
		.ALUCtr_In		(IDEX_ALUCtr_In),										
		.Addr_In			(IDEX_Addr_In),										
		.Tnew_In			(IDEX_Tnew_In),
		.Lui_In			(IDEX_Lui_In),
		.ALUSign_In		(IDEX_ALUSign_In),
		.MemAddrCtr_In	(IDEX_MemAddrCtr_In),
		.MemExtOp_In	(IDEX_MemExtOp_In),
		.MD_In			(IDEX_MD_In),
		.MDCtr_In		(IDEX_MDCtr_In),
		.CP0_Write_In	(IDEX_CP0Write_In),
		.CP0_Read_In	(IDEX_CP0Read_In),
		.BJ_In			(IDEX_BJ_In),
		.ExcCode_In		(IDEX_ExcCode_In),
		.Instr_Out		(IDEX_Instr_Out),
		.PC_Out			(IDEX_PC_Out),
		.RD1_Out			(IDEX_RD1_Out),
		.RD2_Out			(IDEX_RD2_Out),
		.Imm_Out			(IDEX_Imm_Out),
		.RegWrite_Out	(IDEX_RegWrite_Out),
		.MemWrite_Out	(IDEX_MemWrite_Out),
		.MemtoReg_Out	(IDEX_MemtoReg_Out),
		.SavePC_Out		(IDEX_SavePC_Out),
		.ALUSrc_Out		(IDEX_ALUSrc_Out),
		.ALUCtr_Out		(IDEX_ALUCtr_Out),
		.Addr_Out		(IDEX_Addr_Out),
		.Tnew_Out		(IDEX_Tnew_Out),
		.Lui_Out			(IDEX_Lui_Out),
		.ALUSign_Out	(IDEX_ALUSign_Out),
		.MemAddrCtr_Out(IDEX_MemAddrCtr_Out),
		.MemExtOp_Out	(IDEX_MemExtOp_Out),
		.MD_Out			(IDEX_MD_Out),
		.MDCtr_Out		(IDEX_MDCtr_Out),
		.CP0_Write_Out	(IDEX_CP0Write_Out),
		.CP0_Read_Out	(IDEX_CP0Read_Out),
		.BJ_Out			(IDEX_BJ_Out),
		.ExcCode_Out	(IDEX_ExcCode_Out));
	//采用流水线寄存器的数据进行转发，在ALU处只有EXMEM和MEMWB的数据需要考虑
	assign ALU1 =	(IDEX_Instr_Out[25:21] != 5'b0 && IDEX_Instr_Out[25:21] == EXMEM_Addr_Out && EXMEM_RegWrite_Out == 1 && EXMEM_SavePC_Out == 1) ? EXMEM_PC_Out + 8 :
						(IDEX_Instr_Out[25:21] != 5'b0 && IDEX_Instr_Out[25:21] == EXMEM_Addr_Out && EXMEM_RegWrite_Out == 1 && EXMEM_MemtoReg_Out == 0) ? EXMEM_ALURes_Out :
						(IDEX_Instr_Out[25:21] != 5'b0 && IDEX_Instr_Out[25:21] == MEMWB_Addr_Out && MEMWB_RegWrite_Out == 1) ? WriteData : IDEX_RD1_Out;
	assign ALU2 =	(IDEX_ALUSrc_Out == 1) ? IDEX_Imm_Out : 
						(IDEX_Instr_Out[20:16] != 5'b0 && IDEX_Instr_Out[20:16] == EXMEM_Addr_Out && EXMEM_RegWrite_Out == 1 && EXMEM_SavePC_Out == 1) ? EXMEM_PC_Out + 8 :
						(IDEX_Instr_Out[20:16] != 5'b0 && IDEX_Instr_Out[20:16] == EXMEM_Addr_Out && EXMEM_RegWrite_Out == 1 && EXMEM_MemtoReg_Out == 0) ? EXMEM_ALURes_Out :
						(IDEX_Instr_Out[20:16] != 5'b0 && IDEX_Instr_Out[20:16] == MEMWB_Addr_Out && MEMWB_RegWrite_Out == 1) ? WriteData : IDEX_RD2_Out;							
	BuildALU MyALU(																
		.F					(IDEX_ALUCtr_Out),													
		.A					(ALU1),													
		.B					(ALU2),
		.ALUSign			(IDEX_ALUSign_Out),
		.C					(ALURes));	
	assign start =	(IDEX_MD_Out == 1 && IDEX_MDCtr_Out == 3'b000) ? 1'b1 :
						(IDEX_MD_Out == 1 && IDEX_MDCtr_Out == 3'b001) ? 1'b1 :
						(IDEX_MD_Out == 1 && IDEX_MDCtr_Out == 3'b010) ? 1'b1 :
						(IDEX_MD_Out == 1 && IDEX_MDCtr_Out == 3'b011) ? 1'b1 : 1'b0;
	BuildMultDiv MultDiv(
		.ALU1				(ALU1),
		.ALU2				(ALU2),
		.ALUCtr			(IDEX_MDCtr_Out),
		.WE				(~IntReq),
		.start			(start),
		.clk				(clk),
		.busy				(busy),
		.Res				(MDRes));
	assign EXMEM_ALURes_In = (IDEX_MD_Out == 1'b1) ? MDRes : ALURes;
	//写入DM的数据延迟需要暂时存储
	assign EXMEM_RD2_In = (IDEX_Instr_Out[20:16] != 5'b0 && IDEX_Instr_Out[20:16] == A3 && MEMWB_RegWrite_Out == 1) ? WriteData : IDEX_RD2_Out;
	BuildEXMEM EXMEM(																
		.clk				(clk),														
		.reset			(reset),														
		.Instr_In		(IDEX_Instr_Out),														
		.PC_In			(IDEX_PC_Out),															
		.RegWrite_In	(IDEX_RegWrite_Out),															
		.MemWrite_In	(IDEX_MemWrite_Out),															
		.MemtoReg_In	(IDEX_MemtoReg_Out),															
		.SavePC_In		(IDEX_SavePC_Out),															
		.ALUSrc_In		(IDEX_ALUSrc_Out),															
		.ALURes_In		(EXMEM_ALURes_In),															
		.Addr_In			(IDEX_Addr_Out),															
		.Tnew_In			(IDEX_Tnew_Out),															
		.RD2_In			(EXMEM_RD2_In),
		.MemAddrCtr_In	(IDEX_MemAddrCtr_Out),
		.MemExtOp_In	(IDEX_MemExtOp_Out),
		.CP0_Write_In	(IDEX_CP0Write_Out),
		.CP0_Read_In	(IDEX_CP0Read_Out),
		.BJ_In			(IDEX_BJ_Out),
		.ExcCode_In		(IDEX_ExcCode_Out),
		.Instr_Out		(EXMEM_Instr_Out),
		.PC_Out			(EXMEM_PC_Out),
		.RegWrite_Out	(EXMEM_RegWrite_Out),
		.MemWrite_Out	(EXMEM_MemWrite_Out),
		.MemtoReg_Out	(EXMEM_MemtoReg_Out),
		.SavePC_Out		(EXMEM_SavePC_Out),
		.ALUSrc_Out		(EXMEM_ALUSrc_Out),
		.ALURes_Out		(EXMEM_ALURes_Out),
		.Addr_Out		(EXMEM_Addr_Out),
		.RD2_Out			(EXMEM_RD2_Out),
		.Tnew_Out		(EXMEM_Tnew_Out),
		.MemAddrCtr_Out(EXMEM_MemAddrCtr_Out),
		.MemExtOp_Out	(EXMEM_MemExtOp_Out),
		.CP0_Write_Out	(EXMEM_CP0Write_Out),
		.CP0_Read_Out	(EXMEM_CP0Read_Out),
		.BJ_Out			(EXMEM_BJ_Out),
		.ExcCode_Out	(EXMEM_ExcCode_In));
	//采用流水线寄存器进行数据转发
	assign MemIn	= (EXMEM_Instr_Out[20:16] != 0 && EXMEM_Instr_Out[20:16] == MEMWB_Addr_Out) ? WriteData : EXMEM_RD2_Out;															
	assign MemAddr	= EXMEM_ALURes_Out[13:2];						
	assign m_data_addr =  EXMEM_ALURes_Out;
	assign m_inst_addr = EXMEM_PC_Out;
	assign m_data_byteen = (IntReq) ? 4'b0 : Byteen;
	BE BE(
		.MemWrite		(EXMEM_MemWrite_Out),
		.MemAddrCtr		(EXMEM_MemAddrCtr_Out),
		.ALURes			(EXMEM_ALURes_Out),
		.MemIn			(MemIn),
		.Byteen			(Byteen),
		.MemOut			(m_data_wdata)
	);
	BuildMemExt MemExt(
		.Addr				(EXMEM_ALURes_Out),
		.MemData			(m_data_rdata),
		.MemExtOp		(EXMEM_MemExtOp_Out),
		.MemAddrCtr		(EXMEM_MemAddrCtr_Out),
		.MemExtData		(MemOut)
	);
	assign delay = MEMWB_BJ_Out;
	CP0 CP0(
	.A			(EXMEM_Instr_Out[15:11]),
	.DataIn	(MemIn),
	.PC		(CP0_PC_In),
	.ExcCode	(EXMEM_ExcCode_Out),
	.HWInt	(HWInt),
	.WE		(EXMEM_CP0Write_Out),
	.EXLClr	(Eret),
	.clk		(clk),
	.reset	(reset),
	.delay	(delay),
	.IntReq	(IntReq),
	.EPC		(CP0_PC_Out),
	.DataOut	(CP0_DataOut)
	);
	assign MEMWB_ALURes_In = (EXMEM_CP0Read_Out == 1) ? CP0_DataOut : EXMEM_ALURes_Out;
	BuildMEMWB MEMWB(																
		.clk				(clk),													
		.reset			(reset),													
		.Instr_In		(EXMEM_Instr_Out),									
		.PC_In			(EXMEM_PC_Out),										
		.RegWrite_In	(EXMEM_RegWrite_Out),									
		.MemtoReg_In	(EXMEM_MemtoReg_Out),									
		.SavePC_In		(EXMEM_SavePC_Out),										
		.MemData_In		(MemOut),													
		.ALURes_In		(MEMWB_ALURes_In),										
		.Addr_In			(EXMEM_Addr_Out),											
		.Tnew_In			(EXMEM_Tnew_Out),
		.Instr_Out		(MEMWB_Instr_Out),
		.PC_Out			(MEMWB_PC_Out),
		.RegWrite_Out	(MEMWB_RegWrite_Out),
		.MemtoReg_Out	(MEMWB_MemtoReg_Out),
		.SavePC_Out		(MEMWB_SavePC_Out),
		.MemData_Out	(MEMWB_MemData_Out),
		.ALURes_Out		(MEMWB_ALURes_Out),
		.Addr_Out		(MEMWB_Addr_Out),
		.Tnew_Out		(MEMWB_Tnew_Out));									

endmodule
