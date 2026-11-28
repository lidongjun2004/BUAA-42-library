D:\ISE\14.7\ISE_DS\ISE\bin\nt64\fuse.exe -nodebug -prj test.prj -o testmips.exe mips_tb
java -jar Mars4_5.jar nc mc CompactDataAtZero a dump .text HexText code.txt test\testcase0\text.asm
testmips.exe -nolog -tclbatch test.tcl > test\testcase0\out.txt
