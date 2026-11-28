.data
matrix: .space 196
fill: .space 196

.macro get(%dst, %row, %col, %rank)
multu %row, %rank
mflo %dst
addu %dst, %dst, %col
sll %dst, %dst, 2
.end_macro

.macro up(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 0
beq %row, 0, next1
subi %row, %row, 1
get(%index, %row, %col, %maxcol)
lw %tmp, matrix(%index)
beq %tmp, 1, continue1
lw %tmp, fill(%index)
beq %tmp, 1, continue1
li %tmp, 2
continue1:
addi %row, %row, 1
subi %tmp, %tmp, 1
next1:
.end_macro

.macro down(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 0
addi, %row, %row, 1
beq %row, %maxrow, next2
get(%index, %row, %col, %maxcol)
lw %tmp, matrix(%index)
beq %tmp, 1, continue2
lw %tmp, fill(%index)
beq %tmp, 1, continue2
li %tmp, 2
continue2:
subi %tmp, %tmp, 1
next2:
subi %row, %row, 1
.end_macro

.macro left(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 0
beq %col, 0, next3
subi %col, %col, 1
get(%index, %row, %col, %maxcol)
lw %tmp, matrix(%index)
beq %tmp, 1, continue3
lw %tmp, fill(%index)
beq %tmp, 1, continue3
li %tmp, 2
continue3:
addi %col, %col, 1
subi %tmp, %tmp, 1
next3:
.end_macro

.macro right(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 0
addi %col, %col, 1
beq %row, %maxrow,next4
get(%index, %row, %col, %maxcol)
lw %tmp, matrix(%index)
beq %tmp, 1, continue4
lw %tmp, fill(%index)
beq %tmp, 1, continue4
li %tmp, 2
continue4:
subi %tmp, %tmp, 1
next4:
subi %col, %col, 1
.end_macro

.macro judge(%dst, %row, %col, %maxrow, %maxcol, %tmp, %index)
li %dst, 0
up(%row, ,%col, %maxrow, %maxcol, %tmp, %index)
addu %dst, %dst, %tmp
down(%row, ,%col, %maxrow, %maxcol, %tmp, %index)
addu %dst, %dst, %tmp
left(%row, ,%col, %maxrow, %maxcol, %tmp, %index)
addu %dst, %dst, %tmp
right(%row, ,%col, %maxrow, %maxcol, %tmp, %index)
addu %dst, %dst, %tmp
.end_macro

.macro back(%sp, %row, %col, %maxrow, %maxcol, %tmp, %index)
mult %maxrow, %maxcol
mflo %tmp
sll %tmp, %tmp, 2
addu %sp, %sp, %tmp
li %row, 0
back_row:
beq %row, %maxrow, end_back_row
li %col, 0
back_col:
beq %col, %maxcol, end_back_col
lw %tmp, 0(%sp)
subi %sp, %sp, 4
get(%index, %row, %col, %maxcol)
sw %tmp, fill(%index)
addi %col, %col, 1
j back_col
end_back_col:
addi %row, %row, 1
j back_row
end_back_row:
mult %maxrow, %maxcol
mflo %tmp
sll %tmp, %tmp, 2
addu %sp, %sp, %tmp
addi %sp, %sp, 4
lw %col, 0(%sp)
addi %sp, %sp, 4
lw %row, 0(%sp)
subi %sp, %sp, 8
subu %sp, %sp, %tmp
.end_macro

.text
li $v0, 5		##input row, col
syscall
move $s0, $v0	##s0 <- maxrow
li $v0, 5
syscall
move $s1, $v0	##s1 <- maxcol

li $t0, 0		##input matrix
input_row:
beq $t0, $s0, end_input_row
li $t1, 0
input_col:
beq $t1, $s1, end_input_col
li $v0, 5
syscall
get($t2, $t0, $t1, $s1)
sw $v0, matrix($t2)
addi $t1, $t1, 1
j input_col
end_input_col:
addi $t0, $t0, 1
j input_row
end_input_row:

li $v0, 5			##begin end input
syscall
subi $s2, $v0, 1		##s2 <- begin row
li $v0, 5
syscall
subi $s3, $v0, 1		##s3 <- begin col
li $v0, 5
syscall
subi $s4, $v0, 1		##s4 <- end row
li $v0, 5
syscall
subi $s5, $v0, 1		##s5 <- end col

move $t0, $s2
move $t1, $s3
li $s6, 0			##s6 <- cnt
li $t9, 1			##t9 <- 1
jal walk
j end

walk:
bne $t0, $s4, continue_walk
bne $t1, $s5, continue_walk
addi $s6, $s6, 1
jr $ra
continue_walk:
judge($t2, $t0, $t1, $s0, $s1, $t3, $t4)
beq $t2, 1, toup
bne $t2, 0, deep
jr $ra
toup:
up($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, todown
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
subi $t0, $t0, 1
j walk
todown:
down($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, toleft
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
addi $t0, $t0, 1
j walk
toleft:
left($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, toright
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
subi $t1, $t1, 1
j walk
toright:
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
addi $t1, $t1, 1
j walk
deep:

sw $ra, 0($sp)			##save ra
subi $sp, $sp, 4
sw $t0, 0($sp)			##save row
subi $sp, $sp, 4
sw $t1, 0($sp)			##save col
subi $sp, $sp, 4
li $t2, 0				##save fill
save_row:
beq $t2, $s0, end_save_row
li $t3, 0
save_col:
beq $t3, $s1, end_save_col
get($t4, $t2, $t3, $s1)
lw $t5, fill($t4)
sw $t5, 0($sp)
subi $sp, $sp, 4
addi $t3, $t3, 1
j save_col
end_save_col:
addi $t2, $t2, 1
j save_row
end_save_row:

up($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, deep_down
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
subi $t0, $t0, 1
jal walk
back($sp, $t0, $t1, $s0, $s1, $t2, $t3)

deep_down:
down($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, deep_left
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
addi $t0, $t0, 1
jal walk
back($sp, $t0, $t1, $s0, $s1, $t2, $t3)

deep_left:
left($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, deep_right
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
subi $t1, $t1, 1
jal walk
back($sp, $t0, $t1, $s0, $s1, $t2, $t3)

deep_right:
right($t0, $t1, $s0, $s1, $t2, $t3)
beq $t2, 0, end_deep
get($t2, $t0, $t1, $s1)
sw $t9, fill($t2)
addi $t1, $t1, 1
jal walk
back($sp, $t0, $t1, $s0, $s1, $t2, $t3)

end_deep:
mult $s0, $s1
mflo $t2
sll $t2, $t2, 2
addu $sp, $sp, $t2
addi $sp, $sp, 12
lw $ra, 0($sp)
jr $ra

end:
li $v0, 1
move $a0, $s6
syscall
li $v0, 10
syscall