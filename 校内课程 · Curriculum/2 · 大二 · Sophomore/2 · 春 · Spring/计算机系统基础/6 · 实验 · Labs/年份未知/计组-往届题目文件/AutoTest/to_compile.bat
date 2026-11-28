D:\ISE\14.7\ISE_DS\ISE\bin\nt64\fuse.exe -nodebug -prj test.prj -o testmips.exe mips_tb
java -jar Mars.jar nc mc CompactDataAtZero a dump .text HexText code.txt test\testpoint0.asm
testmips.exe -nolog -tclbatch test.tcl > test\testcase0\out.txt
java -jar Mars.jar nc mc CompactDataAtZero a dump .text HexText code.txt test\testpoint1.asm
testmips.exe -nolog -tclbatch test.tcl > test\testcase1\out.txt
java -jar Mars.jar nc mc CompactDataAtZero a dump .text HexText code.txt test\testpoint2.asm
testmips.exe -nolog -tclbatch test.tcl > test\testcase2\out.txt
