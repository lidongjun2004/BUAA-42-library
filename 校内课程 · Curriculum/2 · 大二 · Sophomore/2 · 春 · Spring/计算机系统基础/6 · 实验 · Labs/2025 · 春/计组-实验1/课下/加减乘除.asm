#input section
li $v0, 5
syscall
move $t1, $v0 # t1 = a
li $v0, 5
syscall
move $t2, $v0 # t2 = b
li $v0, 5
syscall
move $t3, $v0 # t3 = op

# branch
beq $t3, 0, label0 # add
beq $t3, 1, label1 # subtract
beq $t3, 2, label2 # multiply
beq $t3, 3, label3 # divide

label0:
add $a0, $t1, $t2
li $v0, 1
syscall
li $v0, 10
syscall

label1:
sub $a0, $t1, $t2
li $v0, 1
syscall
li $v0, 10
syscall

label2:
mul $a0, $t1, $t2
li $v0, 1
syscall
li $v0, 10
syscall

label3:
div $t1, $t2
mflo $a0
li $v0, 1
syscall
li $v0, 10
syscall