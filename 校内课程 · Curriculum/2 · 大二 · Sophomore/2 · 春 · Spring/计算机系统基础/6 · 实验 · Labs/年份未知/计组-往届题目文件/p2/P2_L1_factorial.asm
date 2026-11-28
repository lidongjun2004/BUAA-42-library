.data
arr: .space 1000
.text
li $v0, 5
syscall
addi $s0, $v0, 1		##s0 <- max
li $s1, 4			##s1 <- len
li $s2, 1000000
li $s4, 100000
li $t0, 1
sw $t0, arr($0)
loop:
addi $t0, $t0, 1		##t0 <- i
beq $t0, $s0, end
li $t3, 0
li $t1, 0
mul:
beq $t1, $s1, end_mul
lw $t2, arr($t1)
mult $t2, $t0
mflo $t4
addu $t4, $t4, $t3
div $t4, $s2
mfhi $t4
sw $t4, arr($t1)
mflo $t3
addi $t1, $t1, 4
j mul
end_mul:
beq $t3, 0, loop
sw $t3, arr($s1)
addi $s1, $s1, 4
j loop
end:
subi $t0, $s1, 4
lw $a0, arr($t0)
li $v0, 1
syscall
subi $t0, $t0, 4
out:
li $v0, 1
beq $t0, -4, end_out
lw $s3, arr($t0)
li $a0, 0
slt $t1, $s3, $s4
beq $t1, 1, out1
j out6
out1:
syscall
slti $t1, $s3, 10000
beq $t1, 1, out2
j out6
out2:
syscall
slti $t1, $s3, 1000
beq $t1, 1, out3
j out6
out3:
syscall
slti $t1, $s3, 100
beq $t1, 1, out4
j out6
out4:
syscall
slti $t1, $s3, 10
beq $t1, 1, out5
j out6
out5:
syscall
out6:
move $a0, $s3
syscall
subi $t0, $t0, 4
j out
end_out:
li $v0, 10
syscall