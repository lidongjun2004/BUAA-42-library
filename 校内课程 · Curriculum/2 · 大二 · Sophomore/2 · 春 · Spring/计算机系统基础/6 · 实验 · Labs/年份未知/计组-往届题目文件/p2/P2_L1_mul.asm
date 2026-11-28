.data
	num1: .space 0x0400
	num2: .space 0x0400
	ans: .space 0x0800

.macro getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro

.text
	li $s4, 10
	li $v0, 5
	syscall
	move $s0, $v0
	subi $t0, $s0, 1
	for_1:
	beq $t0, -1, for_1_end
	nop
	li $v0, 5
	syscall
	move $t1, $v0
	getindex($t2, $t0)
	sw $t1, num1($t2)
	subi $t0, $t0, 1
	j for_1
	nop
	for_1_end: 
	############
	li $v0, 5
	syscall
	move $s1, $v0
	subi $t0, $s1, 1
	for_2:
	beq $t0, -1, for_2_end
	nop
	li $v0, 5
	syscall
	move $t1, $v0
	getindex($t2, $t0)
	sw $t1, num2($t2)
	subi $t0, $t0, 1
	j for_2
	nop
	for_2_end: 
	###########
	li $t0, 0
	for_3:
	beq $t0, $s0, for_3_end
	nop
	li $t1, 0
	for_4:
	beq $t1, $s1, for_4_end
	nop
	getindex($t2, $t0)
	lw $t3, num1($t2)	# t3=num1[i]
	getindex($t2, $t1)
	lw $t4, num2($t2)	#t4 =num2[j]
	mult $t3, $t4
	mflo $t5	#t5 = num1[i]*num2[j]
	add $t6, $t0, $t1	#t6 = i+j
	getindex($t2, $t6)
	lw $t7, ans($t2)	#t7= ans[i+j]
	add $t7, $t7, $t5
	div $t7, $s4	#ans[i+j] / 10
	mfhi $t8	#t8 = ans[i+j]mod10
	mflo $t9	#t9 = carry= ans[i+j]/10
	sw $t8, ans($t2)
	addi $t6, $t6, 1	#t6 = i +j +1
	getindex($t2, $t6)
	lw $t5, ans($t2)
	add $t5, $t5, $t9
	sw $t5, ans($t2)
	addi $t1, $t1, 1
	j for_4
	nop
	for_4_end:
	addi $t0, $t0, 1
	j for_3
	nop
	for_3_end:
	##########
	
	li $t0, 511
	for_5:
	beq $t0, 0, for_5_end
	nop
	getindex($t2, $t0)
	lw $t3, ans($t2)
	bne $t3, 0, for_5_end
	
	subi $t0, $t0, 1
	j for_5
	nop
	for_5_end:
	##########
	move $t1, $t0
	for_6:
	beq $t1, -1, for_6_end
	nop
	getindex($t2, $t1)
	lw $t3, ans($t2)
	move $a0, $t3
	li $v0, 1
	syscall
	subi $t1, $t1, 1
	j for_6
	nop
	for_6_end:
	
	li $v0, 10
	syscall