.data
	arr:.space	40
	enter: .asciiz "\n"
.macro	getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro

.text
main:
	li	$v0, 5
	syscall
	move	$s0, $v0
	li	$t0, 0
	for_1:
	beq $t0, $s0, for_1_end
	nop
	addi $t1, $t0, 1
	getindex($t2, $t0)
	sw $t1, arr($t2)
	
	addi $t0, $t0, 1
	j for_1
	for_1_end:
	
	li $a0, 0
	subi $a1, $s0, 1
	jal perm
	
	li $v0, 11
	syscall
	
perm:
	bne $a0, $a1, work
	nop
	sw $a0, 0($sp)
	subi $sp, $sp, 4
	addi $t1, $a1, 1
	
	li $t0, 0
	for_2:
	beq $t0, $t1, for_2_end
	nop
	getindex($t2, $t0)
	lw $a0,  arr($t2)
	li $v0, 1
	syscall
	addi $t0, $t0, 1
	j for_2
	nop
	for_2_end:
	lw $a0, enter
	li $v0, 4
	syscall
	
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	jr $ra
	nop

work: 
	move $t0, $a0
	move $t6, $a0
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	sw $a0, 0($sp)
	subi $sp, $sp, 4
	
	addi $t1, $a1, 1
	for_3:
	beq $t0, $t1, for_3_end
	getindex($t2, $t0)	#t2 = add.i
	lw $t3, arr($t2)	#t3 = arr[i]
	getindex($t4, $t6)	#t4 = add.start
	lw $t5, arr($t4)	#t5 = arr[start]
	sw $t5, arr($t2)
	sw $t3, arr($t4)
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	addi $a0, $a0, 1
	jal perm
	nop
	
	subi $a0, $a0, 1
	
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	
	addi $sp, $sp, 4
	lw $a0, 0($sp)

	getindex($t2, $t0)	#t2 = add.i
	lw $t3, arr($t2)	#t3 = arr[i]
	getindex($t4, $6)	#t4 = add.start
	lw $t5, arr($t4)	#t5 = arr[start]
	sw $t5, arr($t2)
	sw $t3, arr($t4)
	
	addi $t0, $t0, 1
	j for_3
	nop
	for_3_end:
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	jr $ra
	
	
	
