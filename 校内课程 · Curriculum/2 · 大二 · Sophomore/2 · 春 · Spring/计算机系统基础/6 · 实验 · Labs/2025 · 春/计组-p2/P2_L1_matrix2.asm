.data
	str_space: .asciiz " "
	str_enter: .asciiz "\n"
	tmp:.space 0x0100
	result:.space 0x0100
.macro getindex(%ans, %i, %j)
	sll %ans, %i, 3
	add %ans, %ans, %j
	sll %ans, %ans, 2
.end_macro

.text
main:
	li $v0, 5
	syscall 
	move $s0, $v0	#s0 = n
	li $v0, 5
	syscall
	move $s1, $v0	#s1 = m
	###########
	li $t0, 0
	for_1:
	beq $t0, $s1, for_1_end
	nop
	
	li $t1, 0
	for_2:
	beq $t1, $s1, for_2_end
	nop
	li $v0, 5
	syscall
	move $t2, $v0
	getindex($t3, $t0, $t1)
	sw $t2, tmp($t3)
	
	addi $t1, $t1, 1
	j for_2
	nop
	for_2_end:
	addi $t0, $t0, 1
	j for_1
	nop
	for_1_end:
	##########
	jal powerTempMatrix
	
	li $t0, 0
	for_9:
	beq $t0, $s1, for_9_end
	nop
	li $t1, 0
	for_10:
	beq $t1, $s1, for_10_end
	nop
	getindex($t2, $t0, $t1)
	lw $t3, tmp($t2)
	move $a0, $t3
	li $v0, 1
	syscall
	la $a0, str_space
	li $v0, 4
	syscall
	addi $t1, $t1, 1
	j for_10
	nop
	for_10_end:
	la $a0, str_enter
	li $v0, 4
	syscall
	addi $t0, $t0, 1
	j for_9
	nop
	for_9_end:
	li $v0, 10
	syscall
	
	
powerTempMatrix:
	li $t0, 0
	for_3:
	beq $t0, $s0, for_3_end
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	jal sqrtTempMatrix
	nop
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, ($sp)
	###############
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	jal replaceTempMatrix
	nop
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, ($sp)
	addi $t0, $t0, 1
	j for_3
	for_3_end:
	jr $ra
	
sqrtTempMatrix:
	li $t0, 0
	for_4:
	beq $t0, $s1, for_4_end
	li $t1, 0
	for_5:
	beq $t1, $s1, for_5_end
	getindex($t3, $t0, $t1)
	sw $0, result($t3)	#t3 = [i][j].addr
	li $t2, 0
	for_6:
	beq $t2, $s1, for_6_end
	getindex($t4, $t0, $t2)	#t4 = [i][k].addr
	getindex($t5, $t2, $t1)	#t5 = [k][j].addr
	lw $t6, tmp($t4)	#t6 = temp[i][k]
	lw $t7, tmp($t5)	#t7 = temp[k][j]
	lw $t8, result($t3)
	mult $t6, $t7
	mflo $t9
	add $t8, $t8, $t9
	sw $t8, result($t3)
	addi $t2, $t2, 1
	j for_6
	for_6_end:
	addi $t1, $t1, 1
	j for_5
	for_5_end:
	addi $t0, $t0, 1
	j for_4
	for_4_end:
	jr $ra

replaceTempMatrix:
	li $t0, 0
	for_7:
	beq $t0, $s1, for_7_end
	li $t1, 0
	for_8:
	beq $t1, $s1, for_8_end
	getindex($t2, $t0, $t1)
	lw $t3, result($t2)
	sw $t3, tmp($t2)
	addi $t1, $t1, 1
	j for_8
	for_8_end:
	addi $t0, $t0, 1
	j for_7
	for_7_end:
	jr $ra
	
