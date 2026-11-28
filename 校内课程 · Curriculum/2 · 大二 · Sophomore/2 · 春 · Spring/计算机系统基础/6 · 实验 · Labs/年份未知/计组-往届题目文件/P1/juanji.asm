.data
matrix_1: .space  256             
matrix_2: .space  256  
matrix_3: .space  256       
str_enter:  .asciiz "\n"
str_space:  .asciiz " "


.macro  getindex(%ans, %i, %j)
    sll %ans, %i, 3             # %ans = %i * 8
    add %ans, %ans, %j          # %ans = %ans + %j
    sll %ans, %ans, 2           # %ans = %ans * 4
.end_macro

.text
li  $v0, 5
syscall
move $s0, $v0                   # m1
li  $v0, 5
syscall
move $s1, $v0                   # n1
li  $v0, 5
syscall
move $s2, $v0                   # m2
li  $v0, 5
syscall
move $s3, $v0                   # n2

sub $s4,$s0,$s2
addi $s4,$s4,1
sub $s5,$s1,$s3
addi $s5,$s5,1


li  $t0, 0                    
in_i:                          
beq $t0, $s0, in_i_end
li  $t1, 0                   
in_j:                          
beq $t1, $s1, in_j_end
li  $v0, 5
syscall                       
getindex($t2, $t0, $t1)         #($t0 * 8 + $t1) * 4
sw  $v0, matrix_1($t2)            # matrix[$t0][$t1] = $v0
addi $t1, $t1, 1
j   in_j
in_j_end:
addi $t0, $t0, 1
j   in_i
in_i_end:

li $t0,0
read_i:
beq $t0,$s2,read_i_end
li $t1,0
read_j:
beq $t1,$s3,read_j_end
li $v0,5
syscall
getindex($t2,$t0,$t1)
sw $v0, matrix_2($t2)

addi $t1,$t1,1
j read_j
read_j_end:
addi $t0,$t0,1
j read_i
read_i_end:

li $t0,0
#cal_loop:
cal_i:
beq $t0,$s4,cal_i_end
li $t1,0
cal_j:
beq $t1,$s5,cal_j_end

li $t4,0	#g(i,j)
li $t2,0
cal_kerrow:
beq $t2,$s2,cal_kerrow_end
li $t3,0
cal_kercolumn:
beq $t3,$s3,cal_kercolumn_end

add $t8,$t0,$t2
add $t9,$t1,$t3
getindex($t6,$t8,$t9)
lw $t6,matrix_1($t6)
getindex($t7,$t2,$t3)
lw $t7,matrix_2($t7)
mult $t6,$t7
mflo $t5
add $t4,$t4,$t5


addi $t3,$t3,1
j cal_kercolumn
cal_kercolumn_end:
addi $t2,$t2,1
j cal_kerrow
cal_kerrow_end:

getindex($t6,$t0,$t1)
sw $t4,matrix_3($t6)

addi $t1,$t1,1
j cal_j
cal_j_end:
addi $t0,$t0,1
j cal_i
cal_i_end:




li  $t0, 0
out_i:
beq $t0, $s4, out_i_end
li  $t1, 0
out_j:
beq $t1, $s5, out_j_end
getindex($t2, $t0, $t1)
lw  $a0, matrix_3($t2)            # $a0 = matrix[$t0][$t1]
li  $v0, 1
syscall
la  $a0, str_space
li  $v0, 4
syscall                         # 输出一个空格
addi $t1, $t1, 1
j   out_j
out_j_end:
la  $a0, str_enter
li  $v0, 4
syscall                         # 输出一个回车
addi $t0, $t0, 1
j   out_i

out_i_end:
li  $v0, 10
syscall