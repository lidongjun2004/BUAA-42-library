.data
matrix: .space 256

.macro get(%dst, %row, %col)
sll %dst, %row, 3 
addu %dst, %dst, %col
sll %dst, %dst, 2
.end_macro

.macro up(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 1
beq %row, 0, next1
subi %row, %row, 1
get(%index, %row, %col)
lw %tmp, matrix(%index)
addi %row, %row, 1
next1:
.end_macro

.macro down(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 1
addi, %row, %row, 1
beq %row, %maxrow, next2
get(%index, %row, %col)
lw %tmp, matrix(%index)
next2:
subi %row, %row, 1
.end_macro

.macro left(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 1
beq %col, 0, next3
subi %col, %col, 1
get(%index, %row, %col)
lw %tmp, matrix(%index)
addi %col, %col, 1
next3:
.end_macro

.macro right(%row, %col, %maxrow, %maxcol, %tmp, %index)
li %tmp, 1
addi %col, %col, 1
beq %col, %maxcol,next4
get(%index, %row, %col)
lw %tmp, matrix(%index)
next4:
subi %col, %col, 1
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
get($t2, $t0, $t1)
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
li $t7, 1			##t7 <- 1
li $t8, 2			##t8 <- 2
li $t9, 3			##t9 <- 3

walk:					##up <- 0, down <- 1, left <- 2, right <- 3
bne $t0, $s4, toup
bne $t1, $s5, toup
addi $s6, $s6, 1
toup:
up($t0, $t1, $s0, $s1, $t2, $t3)
bne $t2, 0, todown
get($t2, $t0, $t1)
sw $t8, matrix($t2)
sw $0, 0($sp)
subi $sp, $sp, 4
subi $t0, $t0, 1
j walk
todown:
down($t0, $t1, $s0, $s1, $t2, $t3)
bne $t2, 0, toleft
get($t2, $t0, $t1)
sw $t8, matrix($t2)
sw $t7, 0($sp)
subi $sp, $sp, 4
addi $t0, $t0, 1
j walk
toleft:
left($t0, $t1, $s0, $s1, $t2, $t3)
bne $t2, 0, toright
get($t2, $t0, $t1)
sw $t8, matrix($t2)
sw $t8, 0($sp)
subi $sp, $sp, 4
subi $t1, $t1, 1
j walk
toright:
right($t0, $t1, $s0, $s1, $t2, $t3)
bne $t2, 0, back
get($t2, $t0, $t1)
sw $t8, matrix($t2)
sw $t9, 0($sp)
subi $sp, $sp, 4
addi $t1, $t1, 1
j walk

back:
bne $t0, $s2, continue
bne $t1, $s3, continue
j end
continue:
addi $sp, $sp, 4
lw $t2, 0($sp)
beq $t2, 0, backdown
beq $t2, 1, backup
beq $t2, 2, backright
j backleft
backup:
get($t2, $t0, $t1)
sw $0, matrix($t2)
subi $t0, $t0, 1
j toleft

backdown:
get($t2, $t0, $t1)
sw $0, matrix($t2)
addi $t0, $t0, 1
j todown

backleft:
get($t2, $t0, $t1)
sw $0, matrix($t2)
subi $t1, $t1, 1
j back

backright:
get($t2, $t0, $t1)
sw $0, matrix($t2)
addi $t1, $t1, 1
j toright

end:
li $v0, 1
move $a0, $s6
syscall
li $v0, 10
syscall
