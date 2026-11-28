.data
	arr:.space 84

.macro getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro

.text
	li $v0, 5
	syscall
	move $s0, $v0
	
	li $t0, 0
	for_1:
	beq $t0, $s0, for_1_end
	nop
	li $v0, 12
	syscall
	beq $v0, 10, for_1
	nop
	move $t1, $v0
	getindex($t2, $t0)
	sw $t1, arr($t2)
	
	addi $t0, $t0, 1
	j for_1
	nop
	for_1_end:
	
	li $t0, 0
	subi $t1, $s0, 1
	for_2:
	sltu $t5, $t0, $t1
	beq $t5, 0, for_2_end
	nop
	getindex($t2, $t0)
	lw $t3, arr($t2)
	getindex($t2, $t1)
	lw $t4, arr($t2)
	beq $t3, $t4, if_1_else
	li $a0, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	if_1_else:
	addi $t0, $t0, 1
	subi $t1, $t1, 1
	j for_2
	nop
	for_2_end:
	li $a0, 1
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	