.data

matrix: .space 0x4000
space:.asciiz  " "  	#space
enter:.asciiz	"\n"	#\n
.macro getindex(%ans, %i, %j)
	sll %ans, %i, 6
	add %ans, %ans, %j
	addi %ans %ans, 2
	sll %ans, %ans, 2
.end_macro
	
.text
li $v0, 5
syscall
move $s0, $v0	#$s0 = n
li $v0, 5
syscall
move $s1, $v0	#$s1 = m


li $t0 0
in_i:
beq $t0, $s0, in_i_end
nop
li $t1 0
in_j:
beq $t1, $s1, in_j_end
nop
li $v0, 5
syscall
getindex($t2, $t0, $t1)
sw $v0, matrix($t2)
addi $t1, $t1, 1
j in_j
nop
in_j_end:
addi $t0, $t0, 1
j in_i
nop
in_i_end:


subi $t0, $s0, 1	#i = n - 1
out_i:
beq $t0, -1, out_i_end	#for(i = n-1; i >=0; i--)
nop
subi $t1, $s1, 1	#j = m - 1
out_j:
beq $t1, -1, out_j_end	#for(j = m - 1; j >= 0; j--)
nop
getindex($t2, $t0, $t1)
lw $t3, matrix($t2)
beq $t3, 0, if_end	#if(arr[i][j] != 0)
nop

addi $a0, $t0, 1

li $v0, 1
syscall
la $a0, space
li $v0, 4
syscall

addi $a0, $t1, 1
li $v0, 1
syscall
la $a0, space
li $v0, 4
syscall

ori	$a0, $t3, 0
li $v0, 1
syscall
la $a0, space
li $v0, 4
syscall

la $a0, enter
li $v0, 4
syscall

if_end:

subi $t1, $t1, 1	#j--
j out_j
nop
out_j_end:

subi $t0, $t0, 1  #i--
j out_i
nop
out_i_end:














