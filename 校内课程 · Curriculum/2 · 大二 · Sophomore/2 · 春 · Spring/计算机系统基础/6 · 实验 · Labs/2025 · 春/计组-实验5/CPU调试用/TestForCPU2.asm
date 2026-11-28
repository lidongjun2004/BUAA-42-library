 # add sub ori lw sw beq lui nop
 ori $a0 $0 123#a0 = 123
 ori $a1 $a0 456#a1 = 507
 ori $a1 $a1 0#a1 = 507
 ori $a2 0xffff#a2 = 0xffff

 # lui $a3 123#a3 = 0x007B_0000
 ori $t0 1
 subu $t0 $0 $t0
 ori $t0 $t0 0xffff#t0 = 0xffffffff (-1)

 # wrong from here s0 is -1(wrong)
 addu $s0 $a0 $a2#s0 = 65658
 addu $s1 $a0 $t0#s1 = 122
 addu $s2 $t0 $t0#s2 = -2
 addu $s3 $0 $t0#s3 = -1

 subu $s4 $a0 $a1#s4 = -384
 subu $s5 $a1 $a0#s5 = 384
 subu $s6 $t0 $t0#s6 = 0
 subu $s7 $a0 $t0#s7 = 124


 ori $t1 0x0000#t1 = 0
 sw $a0 0($t1)#123
 sw $a2 4($t1)#0xffff
 sw $0 8($t1)#0
 sw $t0 12($t1)#-1
 ori $t2 20#t2 = 20
 sw $a1 -4($t2)#507

 ori $t3 $0 4
 lw $t4 0($t3)#t4 = 0xffff
 lw $t5 4($t3)#t5 = 0
 lw $t6 8($t3)#t6 = -1
 lw $t7 -4($t3)#t7 = 123

 beq $a0 $a1 loop1#unequal
 beq $s3 $t0 loop2#equal

 loop1:lw $t8 0($t1)
 loop2:lw $t8 4($t1)#t8 = 0xffff