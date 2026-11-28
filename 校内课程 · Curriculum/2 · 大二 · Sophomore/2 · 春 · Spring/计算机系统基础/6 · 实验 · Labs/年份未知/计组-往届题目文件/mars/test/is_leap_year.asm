li $v0, 5
syscall

ori $t0, $v0, 0

li $t5, 4
div $t0, $t5
mfhi $t1
bne $t1,$0,if_1_else
nop
ori $t1, $0, 1
j if_1_end
nop
if_1_else:
ori $t1, $0, 0
if_1_end:

li $t5, 100
div $t0, $t5
mfhi $t2
beq $t2,$0,if_2_else
nop
ori $t2, $0, 1
j if_2_end
nop
if_2_else:
ori $t2, $0, 0
if_2_end:

li $t5, 400
div $t0, $t5
mfhi $t3
bne $t3, $0,if_3_else
nop
ori $t3, $0, 1
j if_3_end
nop
if_3_else:
ori $t3, $0, 0
if_3_end:

and $t4, $t1, $t2
or $t4, $t4, $t3

or $a0, $t4, 0
li $v0, 1
syscall