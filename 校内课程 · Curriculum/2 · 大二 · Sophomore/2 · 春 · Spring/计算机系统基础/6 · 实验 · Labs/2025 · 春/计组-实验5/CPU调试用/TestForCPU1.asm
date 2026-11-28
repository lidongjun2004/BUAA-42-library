ori $a3, 1000
ori $a0, 100
ori $t0, 1
ori $t1, 4
ori $s1, 120
sw $a0, 0($s0)
start:
sw $a2, 4($s1)
subu $s1, $s1, $t1
lw $a1, 0($s0)
addu $a2, $a2, $a1
addu $t2, $t2, $t0
beq $a3, $a2, end
ori $a1, 200
j start
end:
ori $s7 999
