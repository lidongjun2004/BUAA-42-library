.data
	symbol:.space 32
	array:.space 32
	str_space:.asciiz " "
	str_enter:.asciiz "\n"
	
.macro getindex(%ans, %i)
	sll %ans, %i, 2
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
	move $a1, $0
	jal full_array
	
	li $v0, 10
	syscall
	
full_array:
	
	#move $t0, $a1	#t0 = index
	#slt $t1, $t0, $s0,	#t1 = (index<n)
	#beq $t1, 1, work
	bne $a1, $s0, work
	nop
	li $t1, 0	#t1 = i
	for_1:
	beq $t1, $s0, for_1_end
	nop
	getindex($t3, $t1)
	lw $a0, array($t3)
	li $v0, 1
	syscall
	print_space
	addi $t1, $t1, 1
	j for_1
	nop
	for_1_end:
	print_enter
	
	jr $31
	
work:
	
	move $s1, $a1	#s1 = index
	li $t2, 0		#t2 = i
	for_2:
	beq $t2, $s0, for_2_end
	nop
	getindex($t3, $t2)		#t3 = i.addr
	lw $t4, symbol($t3)
	#beq $t4, 0, if_yes
	bne $t4, 0, if_2_else
	#if_yes:
	getindex($t5, $s1)	#t5 = index.addr
	addi $t6, $t2, 1
	sw $t6, array($t5)
	li $t7, 1
	getindex($t3, $t2)
	sw $t7, symbol($t3)
	
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $s1, 0($sp)
	subi $sp, $sp, 4
	
	addi $s1, $s1, 1
	move $a1, $s1
	
	jal full_array
	nop
	
	addi $sp, $sp, 4
	lw $s1, 0($sp)
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
	
