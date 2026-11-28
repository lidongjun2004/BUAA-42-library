li $v0, 5
syscall
move $t1, $v0
li $v0, 5
syscall
move $t2, $v0 

label:
beqz $t2, ans
div $t1, $t2
move $t1, $t2
mfhi $t2
jal label

ans:
move $a0, $t1
li $v0, 1
syscall

li $v0, 10
syscall
        
