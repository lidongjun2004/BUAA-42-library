.data
	m1:.space 400
	m2:.space 400
	m3:.space 400
	str_space:.asciiz " "
	str_enter:.asciiz "\n"
	
.macro getindex(%ans, %i, %j)
	li %ans, 10
	mult %ans, %i
	mflo %ans
	add %ans, %ans, %j
	sll %ans, %ans, 2
.end_macro

.text
	li $v0, 5
	syscall
	move $s0, $v0
	li $v0, 5
	syscall
	move $s1, $v0
	li $v0, 5
	syscall
	move $s2, $v0
	li $v0, 5
	syscall
	move $s3, $v0
	
	li $t0, 0
	for_1_i:
	beq $t0, $s0, for_1_i_end
	nop
	li $t1, 0
	for_1_j:
	beq $t1, $s1, for_1_j_end
	nop
	
	li $v0, 5
	syscall
	move $t2, $v0
	getindex($t3, $t0, $t1)
	sw $t2, m1($t3)
	
	addi $t1, $t1, 1
	j for_1_j
	nop
	for_1_j_end:
	
	addi $t0, $t0, 1
	j for_1_i
	nop
	for_1_i_end:
	
	##########################
	
	li $t0, 0
	for_2_i:
	beq $t0, $s2, for_2_i_end
	nop
	li $t1, 0
	for_2_j:
	beq $t1, $s3, for_2_j_end
	nop
	
	li $v0, 5
	syscall
	move $t2, $v0
	getindex($t3, $t0, $t1)
	sw $t2, m2($t3)
	
	addi $t1, $t1, 1
	j for_2_j
	nop
	for_2_j_end:
	
	addi $t0, $t0, 1
	j for_2_i
	nop
	for_2_i_end:
	
	################
	sub $s4, $s0, $s2
	addi $s4, $s4, 1
	sub $s5, $s1, $s3
	addi $s5, $s5, 1
	li $t0, 0
	for_3_i:
	beq $t0, $s4, for_3_i_end
	nop	
	li $t1, 0
	for_3_j:
	beq $t1, $s5, for_3_j_end
	nop
	
	li $t4, 0
	
	li $t2, 0
	for_3_k:
	beq $t2, $s2, for_3_k_end
	nop
	li $t3, 0
	for_3_l:
	beq $t3, $s3, for_3_l_end
	nop
	
	add $t6, $t0, $t2
	add $t7, $t1, $t3
	getindex($t5, $t6, $t7)
	lw $t6, m1($t5)
	move $t5, $t6
	getindex($s6, $t2, $t3)
	lw $t6, m2($s6)
	mult $t5, $t6
	mflo $t5
	##just low
	add $t4, $t4, $t5
	getindex($t5, $t0, $t1)
	sw $t4, m3($t5)
	
	addi $t3, $t3, 1
	j for_3_l
	nop
	for_3_l_end:
	addi $t2, $t2, 1
	j for_3_k
	nop
	for_3_k_end:

	addi $t1, $t1, 1
	nop
	j for_3_j
	nop
	for_3_j_end:
	addi $t0, $t0, 1
	nop
	j for_3_i
	for_3_i_end:
	
	li $t0, 0
	for_4_i:
	beq $t0, $s4, for_4_i_end
	nop
	li $t1, 0
	for_4_j:
	beq $t1, $s5, for_4_j_end
	nop
	getindex($t3, $t0, $t1)
	lw $t2, m3($t3)
	move $a0, $t2
	li $v0, 1
	syscall
	la $a0, str_space
	li $v0, 4
	syscall
	
	addi $t1, $t1, 1
	j for_4_j
	nop
	for_4_j_end:
	la $a0, str_enter
	li $v0, 4
	syscall
	addi $t0, $t0, 1
	j for_4_i
	nop
	for_4_i_end:
	
	li $v0, 10
	syscall