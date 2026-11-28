.macro exit()
    li $v0, 10
    syscall
.end_macro

.macro endl()
    li $v0, 11
    li $a0, 10
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

.macro read_str(%n, %l)
    li $v0, 8
    la $a0, %n
    li $a1, %l
    syscall
.end_macro

.data
    YES: .asciiz "YE5"
    NO: .asciiz "N0"
    str: .space 105
.text
    read_int($t0)
    read_str(str,105)
    addi $t2, $t0, -1
    
    loop:
        bge $t1, $t2, yes
        lb $s1, str($t1)
        lb $s2, str($t2)
        bne $s1, $s2, no
        addi $t1, $t1, 1
        addi $t2, $t2, -1
        j loop
    no:
        print_str(NO)
        exit()
    yes:
        print_str(YES)
        exit()
    
    
    
    
