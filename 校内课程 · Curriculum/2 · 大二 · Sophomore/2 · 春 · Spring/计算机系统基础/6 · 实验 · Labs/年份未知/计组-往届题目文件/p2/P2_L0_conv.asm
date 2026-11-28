.data
m1: .space 400
m2: .space 400
space: .asciiz " "
enter: .asciiz "\n"
.macro get(%dst, %row, %col, %rank)
multu %row, %rank
mflo %dst
addu %dst, %dst, %col
sll %dst, %dst, 2
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
row1:
beq $t0, $s0, end_row1
li $t1, 0
col1:
beq $t1, $s1, end_col1
li $v0, 5
syscall
get($t2, $t0, $t1, $s1)
sw $v0, m1($t2)
addi $t1, $t1, 1
j col1
end_col1:
addi $t0, $t0, 1
j row1
end_row1:

li $t0, 0
row2:
beq $t0, $s2, end_row2
li $t1, 0
col2:
beq $t1, $s3, end_col2
li $v0, 5
syscall
get($t2, $t0, $t1, $s3)
sw $v0, m2($t2)
addi $t1, $t1, 1
j col2
end_col2:
addi $t0, $t0, 1
j row2
end_row2:

sub $s4, $s0, $s2
sub $s5, $s1, $s3
addi $s4, $s4, 1
addi $s5, $s5, 1

li $t0, 0
row:
beq $t0, $s4, end_row
li $t1, 0
col :
beq $t1, $s5, end_col
li $t2, 0
li $a0, 0
##mult
loop_row:
beq $t2, $s2, end_loop_row
li $t3, 0
loop_col:
beq $t3, $s3, end_loop_col
add $t4, $t0, $t2
add $t5, $t1, $t3
get($t6, $t4, $t5, $s1)
lw $s6, m1($t6)
get($t6, $t2, $t3, $s3)
lw $s7, m2($t6)
mult $s6, $s7
mflo $t7
add $a0, $a0, $t7
addi $t3, $t3, 1
j loop_col
end_loop_col:
addi $t2, $t2, 1
j loop_row
end_loop_row:
li $v0, 1
syscall
la $a0, space
li $v0, 4
syscall
##
addi $t1, $t1, 1
j col
end_col:
addi $t0, $t0, 1
la $a0, enter
li $v0, 4
syscall
j row
end_row:
li $v0, 10
syscall