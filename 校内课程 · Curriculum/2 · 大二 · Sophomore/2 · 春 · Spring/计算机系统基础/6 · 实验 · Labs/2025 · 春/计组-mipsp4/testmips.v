`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   13:39:43 11/05/2025
// Design Name:   mips
// Module Name:   G:/buaa/co/mips3/testmips.v
// Project Name:  mips3
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: mips
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module testmips;

	// Inputs
	reg clk;
	reg reset;

	// Instantiate the Unit Under Test (UUT)
	mips uut (
		.clk(clk), 
		.reset(reset)
	);
	always #1 clk=~clk;
	initial begin
		$dumpfile("a.vcd");
		$dumpvars(0, testmips);
		clk = 0;
		reset = 1;
		#10;
		reset=0;
		#2097152;
		$finish;
	end
      
endmodule
// dp.cpp
/*
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned int uint;

void do_assemble() {
	FILE *in=fopen("mars_assemble.txt","r");
	vector<uint> v;
	for(int t;fscanf(in,"%x",&t)!=EOF;v.push_back(t));
	fclose(in);
	cerr<<"assemble size "<<v.size()<<endl;
	while(v.size()<4096) v.push_back(0);
	FILE *out=fopen("code.txt","w");
	for(uint i:v) fprintf(out,"%08x\n",i);
	fclose(out);
}
int main() {
	assert(!system("iverilog *.v"));
	for(ll i=1;i<=1e12;i++) {
		assert(!system("python gen42.py"));
		assert(!system("java -jar Mars_CO_v0.6.1.jar nc mc CompactLargeText se1 a coErr coL1 ig dump 0x3000-0x7000 HexText mars_assemble.txt p4.in"));
		do_assemble();
		assert(!system("java -jar Mars_CO_v0.6.1.jar nc mc CompactLargeText se1 coErr coL1 ig dump 0x0000-0x3000 HexText mars_dump.txt p4.in 2> mars.ans"));
		assert(!system("vvp a.out > verilog.out"));
		if(system("python differ.py")) {
			cout<<"WA #"<<i<<endl;
			return 1;
		}
		cout<<"AC #"<<i<<endl;
	}
	return 0;
}
*/

// gen4.py
/*
from cyaron import *

# 0x3000 ~ 0x6FFF total 0x4000 bytes
# and it is 4096 instructions
# ori reg, reg, [0-65535]
# lui reg, [0-65535]
# add reg, reg, reg
# sub reg, reg, reg
# beq reg, reg, label
# lw reg, offset(reg)
# sw reg, offset(reg)
# jal label
# jr reg
# nop

def reg():
	return f"${randint(0,31)}"
def regno0():
	return f"${randint(1,31)}"
def data(l,r):
	l4=(l+3)//4
	r4=r//4
	return 4*randint(l4,r4)
n=3072
labelid=0
ops=[]
i=0
ops.append(f"add $gp, $0, $0")
ops.append(f"add $sp, $0, $0")
while len(ops)<n:
	i+=1
	r=random.random()
	if r<0.1:
		ops.append(f"op{i}: ori {reg()}, {reg()}, {randint(0,65535)}")
	elif r<0.2:
		ops.append(f"op{i}: lui {reg()}, {randint(0,65535)}")
	elif r<0.25:
		ops.append(f"op{i}: add {reg()}, {reg()}, {reg()}")
	elif r<0.3:
		ops.append(f"op{i}: sub {reg()}, {reg()}, {reg()}")
	elif r<0.4:
		ops.append(f"op{i}: beq {reg()}, {reg()}, op{i+1+randint(1,20)}")
	elif r<0.5:
		ops.append(f"op{i}: lw {reg()}, {data(0x2f80,0x2fff)}($0)")
	elif r<0.6:
		ops.append(f"op{i}: sw {reg()}, {data(0x2f80,0x2fff)}($0)")
	elif r<0.65:
		ops.append(f"op{i}: nop")
	elif r<0.7:
		r1=reg()
		ops.append(f"op{i}: ori {r1}, $0, {data(0x0000,0x0080)}")
		ops.append(f"lw {reg()}, {data(0x0000,0x0080)}({r1})")
	elif r<0.75:
		r1=reg()
		ops.append(f"op{i}: ori {r1}, $0, {data(0x0000,0x0080)}")
		ops.append(f"sw {reg()}, {data(0x0000,0x0080)}({r1})")
	elif r<0.8:
		ops.append(f"op{i}: sw $ra, {data(0x0000,0x0080)}($0)")
	elif r<0.9:
		ops.append(f"op{i}: jal op{i+1+randint(1,20)}")
	else:
		r2=regno0()
		ops.append(f"op{i}: la {r2}, op{i+1+randint(1,20)}")
		ops.append(f"jr {r2}")
test_data = IO("p4.in")
test_data.input_writeln(".data:")
test_data.input_writeln("\tram: .space 0x3000")
test_data.input_writeln(".text:")
for j in range(n):
	test_data.input_writeln(str(ops[j]))
for j in range(i+1,i+30):
	test_data.input_writeln(f"op{j}:")
test_data.close()
*/

// gen42.py
/*
from cyaron import *

# 0x3000 ~ 0x6FFF total 0x4000 bytes
# and it is 4096 instructions
# ori reg, reg, [0-65535]
# lui reg, [0-65535]
# add reg, reg, reg
# sub reg, reg, reg
# beq reg, reg, label
# lw reg, offset(reg)
# sw reg, offset(reg)
# jal label
# jr reg
# nop

def reg():
	# prior 0, 31
	r = random.random()
	if r<0.1:
		return "$0"
	elif r<0.2:
		return "$ra"
	return f"${randint(0,31)}"
def regno0():
	return f"${randint(1,31)}"
def data(l,r):
	l4=(l+3)//4
	r4=r//4
	return 4*randint(l4,r4)


def genALU(sz: int):
	ops = []
	for i in range(sz):
		r = random.random()
		if r<0.1:
			ops.append(f"ori {reg()}, {reg()}, {randint(0,65535)}")
		elif r<0.2:
			ops.append(f"lui {reg()}, {randint(0,65535)}")
		elif r<0.3:
			ops.append(f"add {reg()}, {reg()}, {reg()}")
		elif r<0.4:
			ops.append(f"sub {reg()}, {reg()}, {reg()}")
		elif r<0.5:
			ops.append(f"nop")
		elif r<0.6:
			ops.append(f"lw {reg()}, {data(0x2f80,0x2fff)}($0)")
		elif r<0.7:
			ops.append(f"sw {reg()}, {data(0x2f80,0x2fff)}($0)")
		elif r<0.8:
			r1=reg()
			ops.append(f"ori {r1}, $0, {data(0x0000,0x0080)}")
			ops.append(f"lw {reg()}, {data(0x0000,0x0080)}({r1})")
		elif r<0.9:
			r1=reg()
			ops.append(f"ori {r1}, $0, {data(0x0000,0x0080)}")
			ops.append(f"sw {reg()}, {data(0x0000,0x0080)}({r1})")
		else:
			ops.append(f"sw $ra, {data(0x0000,0x0080)}($0)")
	return ops
ops=[]
ops.append(f"add $gp, $0, $0")
ops.append(f"add $sp, $0, $0")

branches = 1024
for i in range(branches):
	ops.append(f"branch{i}:")
	ops.extend(genALU(randint(0,2)))
	r = random.random()
	if r<0.4:
		ops.append(f"beq {reg()}, {reg()}, branch{randint(i+1,min(i+3,branches))}")
	elif r<0.7:
		ops.append(f"jal branch{randint(i+1,min(i+3,branches))}")
	else:
		ops.append(f"la $at, branch{randint(i+1,min(i+3,branches))}")
		ops.append(f"jr $at")
ops.append(f"branch{branches}:")
# beq reg, reg, label
# jal label
# jr reg

test_data = IO("p4.in")
test_data.input_writeln(".data:")
test_data.input_writeln("\tram: .space 0x3000")
test_data.input_writeln(".text:")
for op in ops:
	test_data.input_writeln(op)
test_data.close()
*/