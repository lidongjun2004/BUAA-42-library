lui $1, 123
sw $1, 12($0)
lw $2, 12($0)
beq $2, $2, next1
nop
lui $3, 123
next1:
sll $2, $2, 2
bne $2, $0, next2
nop
lui $4, 123
next2:
addu $2, $2, $2
bgtz $2, next3
sw $0, 8($0)
lui $5, 123
next3:
ori $2, $2, 1234
bgez $2, next4
nop
lui $6, 123
next4:
lui $1, 65535
sw $1, 12($0)
lw $2, 12($0)
bltz $2, next5
nop
lui $7, 123
next5:
xor $2, $0, $2
blez $2, next6
nop
lui $8, 123
next6:
nop