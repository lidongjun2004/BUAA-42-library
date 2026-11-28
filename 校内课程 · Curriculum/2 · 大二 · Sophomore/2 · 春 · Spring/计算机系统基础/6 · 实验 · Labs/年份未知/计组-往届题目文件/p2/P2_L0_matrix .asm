.data
matrix1: .space 256
matrix2: .space 256
space: .asciiz " "
enter: .asciiz "\n"
.macro get_offset(%dst, %row, %col, %rank)
multu %row, %rank
mflo %dst
addu %dst, %dst, %col
sll %dst, %dst, 2
.end_macro
.text
li $v0, 5
syscall
move $s0, $v0	##S0 <- rank
li $t0, 0
li $t1, 0

row1:
beq $t0, $s0, end_row1
col1:
beq $t1, $s0, end_col1
get_offset($t2, $t0, $t1, $s0)
li $v0, 5
syscall
sw $v0, matrix1($t2)
addi $t1, $t1, 1
j col1
end_col1:
li $t1, 0
addi $t0, $t0, 1
j row1
end_row1:

li $t0, 0
li $t1, 0
row2:
beq $t0, $s0, end_row2
col2:
beq $t1, $s0, end_col2
get_offset($t2, $t0, $t1, $s0)
li $v0, 5
syscall
sw $v0, matrix2($t2)
addi $t1, $t1, 1
j col2
end_col2:
li $t1, 0
addi $t0, $t0, 1
j row2
end_row2:

li $t0, 0
li $t1, 0
li $s1, 0
loop_row:
beq $t0, $s0, end_row
loop_col:
beq $t1, $s0, end_col
li $t4, 0
loop:
beq $t4, $s0, end_loop
get_offset($t5, $t0, $t4, $s0)
lw $t2, matrix1($t5)
get_offset($t5, $t4, $t1, $s0)
lw $t3, matrix2($t5)
multu $t2, $t3
mflo $t6
addu $s1, $s1, $t6
addi $t4, $t4, 1
j loop
end_loop:
li $v0, 1
move $a0, $s1
syscall
li $v0, 4
la $a0, space
syscall
li $s1, 0
addi $t1, $t1, 1
j loop_col
end_col:
li $v0, 4
la $a0, enter
syscall
li $t1, 0
addi $t0, $t0, 1
j loop_row
end_row:
li $v0, 10
syscall