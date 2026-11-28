.data
array: .space 80
.text
li $v0, 5
syscall
move $s0, $v0
li $t0, 0
loop:
beq $t0, $s0, end_loop
li $v0, 12
syscall
sll $t1, $t0, 2
sw $v0, array($t1)
addi $t0, $t0, 1
j loop
end_loop:

subi $t1, $s0, 1
li $t0, 0
loop1:
beq $t0, $s0, end
sll $t2, $t0, 2
sll $t3, $t1, 2
lw $t4, array($t2)
lw $t5, array($t3)
bne $t5, $t4, wrong
addi $t0, $t0, 1
subi $t1, $t1, 1
j loop1
end:
li $a0, 1
j out

wrong:
li $a0, 0

out:
li $v0, 1
syscall
li $v0, 10
syscall