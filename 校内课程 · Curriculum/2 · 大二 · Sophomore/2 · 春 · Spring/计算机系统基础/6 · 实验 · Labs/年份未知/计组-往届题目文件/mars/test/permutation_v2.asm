.data
	arr:.space	40
	enter:.asciiz	"\n"	#\n
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
	sw $a0, 0($sp)
	subi $sp, $sp, 4
	
	bne $a0, $a1, work
	nop
	li $t0, 0
	addi $t1, $a1, 1
	for_2:
	beq $t0, $t1, for_2_end
	getindex($t2, $t0)	#$t2 = i.addr 
	lw $a0, arr($t2)
	li $v0, 1
	syscall
	addi $t0, $t0, 1
	j for_2
	for_2_end:
	
	la $a0, enter
	li $v0, 4
	syscall
	
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	jr $ra

work: 
	
	move $t0, $a0		#t0 = start
	move $t1, $a1		#t1 = end
	
	sw $t1, 0($sp)		#stack <- a1 
	subi $sp, $sp, 4
	sw $t0, 0($sp)		#stack <- a0 = t0
	subi $sp, $sp, 4
	
	ori $t2, $t0, 0		#t2 = i = start
	addi $t1, $t1, 1	#t1 = end + 1	
				
	for_3:
	beq $t2, $t1, for_3_end
	nop
	getindex($t3, $t2)	#t3 = arr[i].addr
	lw $t4, arr($t3)	#t4 = arr[i]
	getindex($t5, $t0)	#t5 = arr[start].addr
	lw $t6, arr($t5)	#t6 = arr[start]
	sw $t4, arr($t5)	#arr[start] = arr[i]
	sw $t6, arr($t3)	#arr[i] = arr[start]
	
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	
	addi $t0, $t0, 1
	move $a0, $t0

	jal perm
	
	
	addi $sp, $sp, 4
	lw $t2, 0($sp)		#i <- stack
	addi $sp, $sp, 4
	lw $t0, 0($sp)		#start <- stack
	move $a0, $t0	
	
	getindex($t3, $t2)	#t3 = arr[i].addr
	lw $t4, arr($t3)	#t4 = arr[i]
	getindex($t5, $t0)	#t5 = arr[start].addr
	lw $t6, arr($t5)	#t6 = arr[start]
	sw $t4, arr($t5)	#arr[start] = arr[i]
	sw $t6, arr($t3)	#arr[i] = arr[start]
	sw $t0, 0($sp)
	
	
	
	addi $t2, $t2, 1
	j for_3
	nop
	for_3_end:
	
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	
	jr $ra
	
	
