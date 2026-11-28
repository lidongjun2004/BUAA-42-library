lui $1, 123
ori $2, $2, 12
sw $2, 12($0)
subu $3, $2, $0
lw $1, 12($0)
jal next
addu $31, $31, $2
lui $2, 123
next:
lui $3, 123
jr $31
lui $2, 123