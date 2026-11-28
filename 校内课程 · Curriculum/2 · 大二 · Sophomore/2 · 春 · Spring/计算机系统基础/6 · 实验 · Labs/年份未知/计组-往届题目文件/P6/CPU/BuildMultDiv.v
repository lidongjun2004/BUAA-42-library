`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:04:28 12/16/2021 
// Design Name: 
// Module Name:    BuildMultDiv 
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
module BuildMultDiv(
    input [31:0] ALU1,
    input [31:0] ALU2,
    input [2:0] ALUCtr,
    input start,
    input clk,
    output reg busy,
    output [31:0] Res
    );

	integer cnt;
	integer max;
	reg [31:0] hi;
	reg [31:0] lo;
	reg [63:0] ans;
	
	always @(posedge clk)
	begin
		if(start == 1)
		begin
			cnt = 0;
			case(ALUCtr)
			3'b000:
			begin
				max = 4;
				ans = $signed(ALU1) * $signed(ALU2);
				hi = ans[63:32];
				lo = ans[31:0];
				busy = 1;
			end
			3'b001:
			begin
				max = 4;
				ans = ALU1 * ALU2;
				hi = ans[63:32];
				lo = ans[31:0];
				busy = 1;
			end
			3'b010:
			begin
				max = 9;
				lo = $signed(ALU1) / $signed(ALU2);
				hi = $signed(ALU1) % $signed(ALU2);
				busy = 1;
			end
			3'b011:
			begin
				max = 9;
				lo = (ALU1 / ALU2);
				hi = (ALU1 % ALU2);
				busy = 1;
			end
			endcase
		end
		else
		begin
			if(cnt < max)
			begin
				busy <= 1;
				cnt <= cnt + 1;
			end
			else
			begin
				busy <= 0;
				case(ALUCtr)
				3'b110:
				begin
					lo = ALU1;
				end
				3'b111:
				begin
					hi = ALU1;
				end
				endcase
			end
		end
	end
	
	assign Res =	(ALUCtr == 3'b100) ? lo :
						(ALUCtr == 3'b101) ? hi : 32'h0;
endmodule
