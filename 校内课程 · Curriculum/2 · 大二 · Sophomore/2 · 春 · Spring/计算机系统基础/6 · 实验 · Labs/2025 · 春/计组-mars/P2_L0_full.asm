.data
symbol: .space 32
arr: .space 32
str_enter: .asciiz"\n"
str_space: .asciiz" "

.macro read_int(%n)
	li $v0, 5
	syscall
	move %n, $v0
.end_macro

.macro print_int(%n)
	move $a0, %n
	li $v0, 1
	syscall
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

.macro getindex(%ans, %i)
	sll %ans, %i, 2
.end_macro


.text
	li $gp, 1
	read_int($s0)
	
	move $a0, $0
	jal full

	li $v0, 10
	syscall


full:
	bne $a0, $s0, work
	li $t0, 0
	output:
		beq $t0, $s0, output_end
		getindex($t1, $t0)
		lw $t2, arr($t1)
		print_int($t2)
		print_space
		addi $t0, $t0, 1
		j output
	output_end:
		print_enter
	jr $31

work:
	
	move $s7, $a0   # $s7: index
	li $t3, 0   # $t3: i
	loop:
		beq $t3, $s0, loop_end  
		getindex($t4, $t3) 
		lw $t4, symbol($t4)  # $t4: symbol[i]
		beq $t4, 0, if_yes
		bne $t4, 0, if_not
		if_yes:
			getindex($s6, $s7)
			addi $t4, $t3, 1
			sw $t4, arr($s6)
			getindex($t4, $t3)
			sw $gp, symbol($t4)
			
			
			sw $ra, 0($sp)
			subi $sp, $sp, 4
			sw $t3, 0($sp)
			subi $sp, $sp, 4
			sw $s7, 0($sp)
			subi $sp, $sp, 4
			
			addi $s7, $s7, 1
			move $a0, $s7
			jal full
			
			addi $sp, $sp, 4
			lw $s7, 0($sp)
			addi $sp, $sp, 4
			lw $t3, 0($sp)
			addi $sp, $sp, 4
			lw $ra, 0($sp)
		
								
			getindex($t4, $t3)
			sw $0, symbol($t4)

		if_not:
		addi $t3, $t3, 1
		j loop
	loop_end:
	jr $31
