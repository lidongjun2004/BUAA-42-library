.data
array: .space 24
fill: .space 24
space: .asciiz " "
enter: .asciiz "\n"
.text
li $v0 5
syscall
move $s0, $v0
li $t0, 0	##t0 <- index
li $t1, 0	##t1 <- num
li $s1, 1	##s1 <- 1const
loop:
beq $t0, $s0, backindex
beq $t1, $s0, back	
sll $t2, $t1, 2
lw $t3, fill($t2)
beq $t3, 1, continue
sw $s1, fill($t2)
sll $t2, $t0, 2
sw $t1, array($t2)
addi $t0, $t0, 1
li $t1, 0
j loop

continue:
addi $t1, $t1, 1
j loop

backindex:
li $t4, 0
out:
beq $t4, $s0, end_out
sll $t3, $t4, 2
lw $a0, array($t3)
addi $a0, $a0, 1
li $v0, 1
syscall
la $a0, space
li $v0, 4
syscall
addi $t4, $t4, 1
j out
end_out:
la $a0, enter
li $v0, 4
syscall
subi $t0, $t0, 1
sll $t2, $t0, 2
lw $t3, array($t2)
addi $t1, $t3, 1
sll $t3, $t3, 2
sw $0, fill($t3)
j loop

back:
beq $t0, 0, end
subi $t0, $t0, 1
sll $t2, $t0, 2
lw $t3, array($t2)
addi $t1, $t3, 1
sll $t3, $t3, 2
sw $0, fill($t3)
j loop

end:
li $v0, 10
syscall