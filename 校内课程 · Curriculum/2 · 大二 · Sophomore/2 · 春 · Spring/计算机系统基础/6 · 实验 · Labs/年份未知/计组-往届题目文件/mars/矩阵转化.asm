.data
array: .space 10000
str_space: .asciiz " "
str_enter: .asciiz "\n"
.macro getindex(%ans, %i, %j)
	mul %ans, %i, 50
	add %ans, %ans, %j
	sll %ans, %ans, 2
.end_macro

.text
li $v0, 5
syscall
move $t0, $v0		##t0 <- row
li $v0, 5
syscall
move $t1, $v0		##t1 <- col
li $t2, 0			##t2 <- count row

in_row:
beq $t2, $t0, in_row_end
li $t3, 0			##t3 <- count col
in_col:
beq $t3, $t1, in_col_end
li $v0, 5
syscall
move $s0, $v0		##s0 <- num
li $s1, 0			##s1 <- index
getindex($s1, $t2, $t3)
sw $s0, array($s1)
addi $t3, $t3, 1
j in_col
in_col_end:
addi $t2, $t2, 1
j in_row
in_row_end:
sub $t2, $t0, 1

out_row:
beq $t2, -1, out_row_end
sub $t3, $t1, 1
out_col:
beq $t3, -1, out_col_end
getindex($s1, $t2, $t3)
lw $s0, array($s1)
beq $s0, 0, continue
addi $a0, $t2, 1
li $v0, 1
syscall
la $a0, str_space
li $v0, 4
syscall
addi $a0, $t3, 1
li $v0, 1
syscall
la $a0, str_space
li $v0, 4
syscall
move $a0, $s0
li $v0, 1
syscall
la $a0, str_enter
li $v0, 4
syscall
continue:
sub $t3, $t3, 1
j out_col
out_col_end:
sub $t2, $t2, 1
j out_row
out_row_end:
li $v0, 10
syscall