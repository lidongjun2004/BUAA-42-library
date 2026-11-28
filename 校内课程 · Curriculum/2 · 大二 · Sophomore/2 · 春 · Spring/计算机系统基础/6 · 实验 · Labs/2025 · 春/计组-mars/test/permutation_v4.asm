.data
	flag:.space 40
	arr:.space 40
	enter:.asciiz "\n"
	
.macro getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro

.text
main:
	li $v0, 5
	syscall
	move $s0, $v0
	li $v0 0
	move $a1, $s0
	jal perm
	
	li $v0, 10
	syscall
	
perm:
	
	#sw $a0, 0($sp)
	#subi $sp, $sp, 4
	#sw $a1, 0($sp)
	#subi $sp, $sp, 4
	move $t6, $a0
	move $t7, $a1
	bne $a0, $a1 if_1_end
	li $t0, 0
	ori $t1, $a1, 0
	for_1:
	beq $t0, $t1, for_1_end
	nop
	getindex($t2, $t0)
	lw $a0, arr($t2)
	li $v0, 1
	syscall
	addi $t0, $t0, 1
	j for_1
	nop
	for_1_end:
	la $a0, enter
	li $v0, 4
	syscall
	jr $ra
	
	if_1_end:
	li $t0, 1
	for_2:
	beq $t0, $t6, for_2_end
	nop
	getindex($t2, $t0)	#t2 == i.addr
	lw $t1, flag($t2)
	bne $t1, 0, if_2_else
	nop
	li $t4, 1
	sw $t4, flag($t2)
	getindex($t2, $t6)	#t2= st.addr
	addi $t3, $t0, 1
	sw $t3, arr($t2)
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	addi $a0, $a0, 1
	jal perm
	nop
	
	subi $a0, $a0, 1
	
	
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	getindex($t2, $t0)
	li $t4, 0
	sw $t4, flag($t2)
	
	if_2_else:
	addi $t0, $t0, 1
	j for_2
	nop
	for_2_end:
	
	jr $ra
	