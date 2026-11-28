li $v0, 5
syscall
move $t1, $v0 # t1 = year
li $t2, 4
li $t3, 100
li $t4, 400

div $t1, $t2
mfhi $t2 # t2 = year % 4
div $t1, $t3
mfhi $t3 # t3 = year % 100
div $t1, $t4
mfhi $t4 # t4 = year % 400

beqz $t4, label1 # year % 400 == 0
beqz $t3, label0 # year % 100 == 0 && year % 400 != 0
beqz $t2, label1 # year % 4 == 0 && year % 100 != 0
b label0


label0: # printf 0
li $a0, 0
li $v0, 1
syscall
li $v0, 10
syscall


label1: # printf 1
li $a0, 1
li $v0, 1
syscall
li $v0, 10
syscall