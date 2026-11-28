lui $0, 100
lui $8, 123
addu $9, $8, $0
addu $10, $8, $8
subu $11, $10, $8
ori $12, $8, 321
next:
sw $8, 120($0)
lw $13, 120($0)
beq $8, $10, next
beq $8, $9, next1
subu $8, $8, $8
next1:
jal next2
addu $15, $8, $8
beq $15, $15, next3
next2:
addu $14, $10, $10
jr $ra
next3:
addu $16, $8, $0