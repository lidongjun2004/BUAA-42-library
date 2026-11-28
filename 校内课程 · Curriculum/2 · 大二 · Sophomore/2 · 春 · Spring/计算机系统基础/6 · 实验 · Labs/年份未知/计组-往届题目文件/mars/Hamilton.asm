.data
	edge:.space 256
	symbol:.space 32
	array:.space 32
	str_space:.asciiz " "
	str_enter:.asciiz "\n"
	
.macro getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro

.macro getmatrix(%ans, %i, %j)
	sll %ans, %i, 3
	add %ans, %ans, %j
	sll %ans %ans, 2
.end_macro

.macro print_space
	la $a0, str_space
	li $v0, 4
	syscall
.end_macro

.macro print_enter
	la $a0, str_enter
	li $v0, 4
	syscall
.end_macro
	
.text
main:
	li $v0, 5
	syscall
	move $s0, $v0
	li $v0, 5
	syscall
	move $s1, $v0
	addedge:
	li $t0, 0
	for_7:
	beq $t0, $s1, for_7_end1
	nop
	li $v0, 5
	syscall
	move $s3, $v0
	li $v0, 5
	syscall
	move $s4, $v0
	getmatrix($s5, $s3, $s4)
	li $s6, 1
	sw $s6, edge($s5)
	getmatrix($s5, $s4, $s3)
	sw $s6, edge($s5)
	
	addi $t0, $t0, 1
	j for_7
	nop
	
	for_7_end1:
	bne $s0, 1, if_9_else
	li $a0, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	if_9_else:
	beq $s0, 2, if_6_yes
	bne $s0, 2, if_6_no 
	if_6_yes:
		li $t0, 1
		li $t1, 2
		getmatrix($t3, $t0, $t1)
		lw $t4, edge($t3)
		beq $t4, 0, if_7_no
		beq $t4, 1, if_7_yes
		if_7_no:
		li $a0, 0
		li $v0, 1
		syscall
		li $v0, 10
		syscall
		if_7_yes:
		li $a0, 1
		li $v0, 1
		syscall
		li $v0, 10
		syscall
	
	if_6_no:
	move $a1, $0
	jal full_array
	
	li $a0, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
full_array:
	
	#move $t0, $a1	#t0 = index
	#slt $t1, $t0, $s0,	#t1 = (index<n)
	#beq $t1, 1, work
	bne $a1, $s0, work
	nop
	li $s3, 1
	li $s4, 0
	li $s5, 0
	li $t1, 0	#t1 = i
	getindex($t3, $t1)
	lw $s4, array($t3)
	addi $t1, $t1, 1
	for_1:
	beq $t1, $s0, for_1_end
	nop
	getindex($t3, $t1)
	lw $s5, array($t3)
	getmatrix($s6, $s4, $s5)
	lw $s7, edge($s6)
	beq $s7, 1, if_3_else
	nop
	li $s3, 0
	if_3_else:
	move $s4, $s5
	addi $t1, $t1, 1
	j for_1
	nop
	for_1_end:
	li $t1, 0
	getindex($t3, $t1)
	lw $s4, array($t3)
	getmatrix($s6, $s5, $s4)
	lw $s7, edge($s6)
	beq $s7, 1, if_5_else
	nop
	li $s3, 0
	if_5_else:
	
	beq $s3, 0, if_4_else
	nop
	li $a0, 1
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	if_4_else:
	
	jr $31
	
work:
	
	move $s2, $a1	#s2 = index
	li $t2, 0		#t2 = i
	for_2:
	beq $t2, $s0, for_2_end
	nop
	getindex($t3, $t2)		#t3 = i.addr
	lw $t4, symbol($t3)
	#beq $t4, 0, if_yes
	bne $t4, 0, if_2_else
	#if_yes:
	getindex($t5, $s2)	#t5 = index.addr
	addi $t6, $t2, 1
	sw $t6, array($t5)
	li $t7, 1
	getindex($t3, $t2)
	sw $t7, symbol($t3)
	
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $s2, 0($sp)
	subi $sp, $sp, 4
	
	addi $s2, $s2, 1
	move $a1, $s2
	
	jal full_array
	nop
	
	addi $sp, $sp, 4
	lw $s2, 0($sp)
	addi $sp, $sp,  4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	
	getindex($t3, $t2)
	sw $0 symbol($t3)
	
	if_2_else:
	addi $t2, $t2, 1
	j for_2
	nop
	for_2_end:
	jr $ra
	
