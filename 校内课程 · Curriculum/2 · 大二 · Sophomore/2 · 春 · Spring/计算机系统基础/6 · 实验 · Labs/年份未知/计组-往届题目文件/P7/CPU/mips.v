`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:26:38 11/18/2021 
// Design Name: 
// Module Name:    mips 
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
module mips(
    input clk,
    input reset,
	 input interrupt,
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
	 output [31:0] macroscopic_pc
    );
	//CPU
	wire [31:0] CPU_Addr;
	wire [31:0] CPU_WriteData;
	wire [31:0] CPU_ReadData;
	wire [3:0] CPU_Byteen;
	wire CPU_Interrupt;
	wire [1:0] CPU_InterruptCtr;
	
	//Bridge
	wire [31:0] Bridge_ReadData;
	wire Time0_Write;
	wire Time1_Write;
	
	//Time0
	wire [31:0] Time0_ReadData;
	wire Time0_Interrupt;
	
	//Time1
	wire [31:0] Time1_ReadData;
	wire Time1_Interrupt;
	
	
	assign CPU_Interrupt = (Time0_Interrupt || Time1_Interrupt || interrupt);
	assign CPU_InterruptCtr =	(Time0_Interrupt) ? 2'b00 :
										(Time1_Interrupt) ? 2'b01 :
										(interrupt) ? 2'b10 : 2'b00;
	BuildCPU MyCPU(
	.clk				(clk),
   .reset			(reset),
	.interrupt		(CPU_Interrupt),
	.interruptCtr	(CPU_InterruptCtr),
   .i_inst_rdata	(i_inst_rdata),
   .m_data_rdata	(Bridge_ReadData),
   .i_inst_addr	(i_inst_addr),
   .m_data_addr	(CPU_Addr),
   .m_data_wdata	(m_data_wdata),
   .m_data_byteen	(CPU_Byteen),
	.m_inst_addr	(m_inst_data),
   .w_grf_we		(w_grf_we),
   .w_grf_addr		(w_grf_addr),
   .w_grf_wdata	(w_grf_wdata),
   .w_inst_addr	(w_inst_addr)
	 );
	
	BuildBridge MyBridge(
	.WE					(CPU_Byteen),
	.Addr					(CPU_Addr),
	.ReadData_Time0	(Time0_ReadData),
	.ReadData_Time1	(Time1_ReadData),
	.ReadData_DM		(m_data_rdata),
	.ReadData			(Bridge_ReadData),
	.MemWrite			(m_data_byteen),
	.Time0_Write		(Time0_Write),
	.Time1_Write		(Time1_Write)
	);
	
	TC Time0(
	clk	(clk),
   reset	(reset),
   Addr	(CPU_Addr),
   WE		(Time0_Write),
   Din	(CPU_WriteData),
   Dout	(Time0_ReadData),
   IRQ	(Time0_Interrupt)
	);
	
	TC Time1(
	clk	(clk),
   reset	(reset),
   Addr	(CPU_Addr),
   WE		(Time1_Write),
   Din	(CPU_WriteData),
   Dout	(Time1_ReadData),
   IRQ	(Time1_Interrupt)
	);

endmodule
