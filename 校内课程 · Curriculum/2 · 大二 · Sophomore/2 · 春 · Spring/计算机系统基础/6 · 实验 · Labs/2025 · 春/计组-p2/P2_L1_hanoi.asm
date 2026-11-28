.data
	.enter: .asciiz "\n"
	.str1: .asciiz	"move disk "
	.str2:	.asciiz	" from "
	.str3:	.asciiz	" to "
	
.text
main:
	li $v0, 5
	syscall
	move $s0, $v0
	move $a0, $s0
	li $a1, 65	#a1 = from	1=='A'
	li $a2, 66	#a2 = via	2=='B'
	li $a3, 67	#a3 = to	3=='C'
	jal hanoi
	nop
	li $v0, 10
	syscall
	
hanoi:
	move $t0, $a0
	move $t1, $a1
	move $t2, $a2
	move $t3, $a3
	if_1:
	bne $a0, $0, if_1_else
	nop
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	move $a1, $t0
	move $a2, $t1
	move $a3, $t2
	jal moval
	nop
	
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	move $a1, $t0
	move $a2, $t2
	move $a3, $t3
	jal moval
	nop
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	jr $ra
	nop
	if_1_else:
	##########	hanoi1
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	subi $a0, $t0, 1
	move $a1, $t1
	move $a2, $t2
	move $a3, $t3
	jal hanoi
	nop
	
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	
	#######	moval1
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	move $a1, $t0
	move $a2, $t1
	move $a3, $t2
	
	jal moval
	nop
	
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	####### hanoi2
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	subi $a0, $t0, 1
	move $a1, $t3
	move $a2, $t2
	move $a3, $t1
	jal hanoi
	nop
	
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	
	####### moval2
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	move $a1, $t0
	move $a2, $t2
	move $a3, $t3
	jal moval
	nop
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	####### hanoi3
	sw $t3, 0($sp)
	subi $sp, $sp, 4
	sw $t2, 0($sp)
	subi $sp, $sp, 4
	sw $t1, 0($sp)
	subi $sp, $sp, 4
	sw $t0, 0($sp)
	subi $sp, $sp, 4
	sw $ra, 0($sp)
	subi $sp, $sp, 4
	
	subi $a0, $t0, 1
	move $a1, $t1
	move $a2, $t2
	move $a3, $t3
	jal hanoi
	nop
	
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $t3, 0($sp)
	#############
	jr $ra
	nop
moval:
	la $a0, .str1
	li $v0, 4
	syscall
	move $a0, $a1
	li $v0, 1
	syscall
	la $a0, .str2
	li $v0, 4
	syscall
	
	move $a0, $a2
	li $v0, 11
	syscall
	la $a0, .str3
	li $v0, 4
	syscall
	move $a0, $a3
	li $v0, 11
	syscall
	la $a0, .enter
	li $v0, 4
	syscall
	jr $ra
	nop
	
