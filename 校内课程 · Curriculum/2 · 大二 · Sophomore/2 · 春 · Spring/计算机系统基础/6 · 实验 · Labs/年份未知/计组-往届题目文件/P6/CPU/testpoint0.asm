
END3:
ori $1, $0, 16084
jalr $ra, $1
nop
j END4
nop
nop
jr $ra
nop
END4:

ori $t0, $0, 16112
add $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16132
add $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16156
add $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16172
addu $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16192
addu $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16216
addu $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16232
sub $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16252
sub $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16276
sub $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16292
subu $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16312
subu $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16336
subu $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t1, $0, 0xffff
ori $t0, $0, 16356
and $1, $t0, $t1
jalr $ra, $1
nop
ori $t1, $0, 0xffff
ori $t0, $0, 16380
and $1, $t0, $t1
nop
jalr $ra, $1
nop
ori $t1, $0, 0xffff
ori $t0, $0, 16408
and $1, $t0, $t1
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16424
or $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16444
or $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16468
or $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, -16493
nor $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, -16521
nor $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, -16553
nor $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16568
xor $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16588
xor $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16612
xor $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16628
sllv $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16648
sllv $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16672
sllv $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16688
srlv $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16708
srlv $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16732
srlv $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16748
srav $1, $t0, $0
jalr $ra, $1
nop
ori $t0, $0, 16768
srav $1, $t0, $0
nop
jalr $ra, $1
nop
ori $t0, $0, 16792
srav $1, $t0, $0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16808
addi $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 16828
addi $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 16852
addi $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16868
addiu $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 16888
addiu $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 16912
addiu $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16928
andi $1, $t0, 0xffff
jalr $ra, $1
nop
ori $t0, $0, 16948
andi $1, $t0, 0xffff
nop
jalr $ra, $1
nop
ori $t0, $0, 16972
andi $1, $t0, 0xffff
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 16988
ori $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 17008
ori $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 17032
ori $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17048
xori $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 17068
xori $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 17092
xori $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17108
sll $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 17128
sll $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 17152
sll $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17168
srl $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 17188
srl $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 17212
srl $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17228
sra $1, $t0, 0x0
jalr $ra, $1
nop
ori $t0, $0, 17248
sra $1, $t0, 0x0
nop
jalr $ra, $1
nop
ori $t0, $0, 17272
sra $1, $t0, 0x0
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17292
mthi $t0
mfhi $1
jalr $ra, $1
nop
ori $t0, $0, 17316
mthi $t0
mfhi $1
nop
jalr $ra, $1
nop
ori $t0, $0, 17344
mthi $t0
mfhi $1
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17364
mtlo $t0
mflo $1
jalr $ra, $1
nop
ori $t0, $0, 17388
mtlo $t0
mflo $1
nop
jalr $ra, $1
nop
ori $t0, $0, 17416
mtlo $t0
mflo $1
nop
nop
jalr $ra, $1
nop

ori $t0, $0, 17436
sw $t0, 0($0)
lw $1, 0($0)
jalr $ra, $1
nop
ori $t0, $0, 17460
sw $t0, 0($0)
lw $1, 0($0)
nop
jalr $ra, $1
nop
ori $t0, $0, 17488
sw $t0, 0($0)
lw $1, 0($0)
nop
nop
jalr $ra, $1
nop
ori $t0, $0, 17508
sh $t0, 0($0)
lh $1, 0($0)
jalr $ra, $1
nop
ori $t0, $0, 17532
sh $t0, 0($0)
lh $1, 0($0)
nop
jalr $ra, $1
nop
ori $t0, $0, 17560
sh $t0, 0($0)
lh $1, 0($0)
nop
nop
jalr $ra, $1
nop
ori $t0, $0, 17580
sh $t0, 0($0)
lhu $1, 0($0)
jalr $ra, $1
nop
ori $t0, $0, 17604
sh $t0, 0($0)
lhu $1, 0($0)
nop
jalr $ra, $1
nop
ori $t0, $0, 17632
sh $t0, 0($0)
lhu $1, 0($0)
nop
nop
jalr $ra, $1
nop
jal TAG79
nop
j END5
nop
TAG79:
jalr $0, $ra
nop
END5:
jal TAG80
nop
j END6
nop
TAG80:
nop
jalr $0, $ra
nop
END6:

ori $1, $0, 17704
jalr $ra, $1
nop
j END7
nop
jalr $0, $ra
nop
END7:
ori $1, $0, 17732
jalr $ra, $1
nop
j END8
nop
nop
jalr $0, $ra
nop
END8:

