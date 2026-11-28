.data
symbol: .space 28
array: .space 28
enter: .asciiz "\n" 
space: .asciiz " "
.text
main:
li $v0,5
syscall
move $s0,$v0	#n
addi $s1,$s0,-1
li $s3,0
li $s4,1
li $a1,0
jal fullarray	#($a1=n,f*=.this*)


li $v0,10
syscall

fullarray:
move $t1,$a1
bne $a1,$s0,work

li $t9,0
print:
beq $t9,$s0,print_end
sll $t8,$t9,2
lw $a0,array($t8)
li $v0,1
syscall		#else:loopbottom:return:
la $a0,space
li $v0,4
syscall
addi $t9,$t9,1
j print
print_end:
la $a0,enter
syscall
jr $ra

work:
li $t0,0

for_loop:
beq $t0,$s0,for_loop_end

if:
sll $t8,$t0,2
lw $t7,symbol($t8)
bne $t7,0,else


addi $t2,$t0,1
sll $t8,$t1,2
sw $t2,array($t8)
sll $t8,$t0,2
sw $s4,symbol($t8)

sw $ra,0($sp)
subi $sp,$sp,4
sw $t1,0($sp)
subi $sp,$sp,4
sw $t0,0($sp)
subi $sp,$sp,4

addi $t1,$t1,1
move $a1,$t1
jal fullarray	#f(n-1,*=.this*)

addi $sp,$sp,4
lw $t0,0($sp)
addi $sp,$sp,4
lw $t1,0($sp)
addi $sp,$sp,4
lw $ra,0($sp)
sll $t8,$t0,2
sw $s3,symbol($t8)



else:
addi $t0,$t0,1
j for_loop
for_loop_end:

jr $ra
















