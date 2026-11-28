.macro exit()
    li $v0, 10
    syscall
.end_macro

.macro endl()
    li $v0, 11
    li $a0, 10
    syscall
.end_macro

.macro dot()
    li $v0, 11
    li $a0, 44
    syscall
.end_macro

.macro print_int(%n)
    li $v0, 1
    move $a0, %n
    syscall
.end_macro

.macro read_int(%n)
    li $v0, 5
    syscall
    move %n, $v0
.end_macro

.macro print_char(%n)
    li $v0, 11
    move $a0, %n
    syscall
.end_macro

.macro read_char(%n)
    li $v0, 12
    syscall
    move %n, $v0
.end_macro

.macro print_str(%n)
    li $v0, 4
    la $a0, %n
    syscall
.end_macro

.macro print_reg_str(%n)
    li $v0, 4
    la $a0, (%n)
    syscall
.end_macro

.macro read_str(%n, %l)
    li $v0, 8
    la $a0, %n
    li $a1, %l
    syscall
.end_macro

.macro swap(%a, %b)
    move $s7, %a
    move %a, %b
    move %b, $s7
.end_macro

.macro print(%from, %to)
    print_reg_str(%from)
    print_str(arrow)
    print_reg_str(%to)
    endl()
.end_macro

.macro check(%num, %from, %to)
    bgt %num, 1, else
        print(%from, %to)
        jr $ra
    else:
.end_macro

.macro hanoi(%num,%from, %via, %to)
    move $t0, %num
    move $t1, %from
    move $t2, %via
    move $t3, %to
    jal hanoi
    j end
    hanoi:
        check($t0, $t1, $t3)
        addi $sp, $sp, -20
        sw $ra, 0($sp)
        sw $t0, 4($sp)
        sw $t1, 8($sp)
        sw $t2, 12($sp)
        sw $t3, 16($sp)
        swap($t2, $t3)
        addi $t0, $t0, -1
        jal hanoi
        lw $t0, 4($sp)
        lw $t1, 8($sp)
        lw $t2, 12($sp)
        lw $t3, 16($sp)
        print($t1, $t3)
        swap($t1, $t2)
        addi $t0, $t0, -1
        jal hanoi
        lw $ra, 0($sp)
        lw $t0, 4($sp)
        lw $t1, 8($sp)
        lw $t2, 12($sp)
        lw $t3, 16($sp)
        addi $sp, $sp, 20
        jr $ra
    
.end_macro
.data
    A: .asciiz "A"
    B: .asciiz "B"
    C: .asciiz "C"
    arrow: .asciiz "->"
.text
    read_int($s0)
    la $t1, A
    la $t2, B
    la $t3, C
    hanoi($s0, $t1, $t2, $t3)
    end:
    exit()
    
    
