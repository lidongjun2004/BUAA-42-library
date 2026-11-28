ori $1, 123
sw $1, 1($1)
jal next
lw $2, 1($1)
next:
lui $2, 321