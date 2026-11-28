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

.macro read_str(%n, %l)
    li $v0, 8
    la $a0, %n
    li $a1, %l
    syscall
.end_macro

.macro bubble_sort(%arr, %len)
    li $t1, 0
    loopi:
        bge $t1, %len, loopi_end
        li $t2, 0
        sub $t0, %len, $t1
        loopj:
            bge $t2, $t0, loopj_end
            mul $t3, $t2, 4
            addi $t4, $t3, 4
            lw $t5, %arr($t3)
            lw $t6, %arr($t4)
            ble $t5, $t6, if_out
                move $t7, $t5
                move $t5, $t6
                move $t6, $t7
                sw $t5, %arr($t3)
                sw $t6, %arr($t4)
            if_out:
            addi $t2, $t2, 1
            j loopj
        loopj_end:
        addi $t1, $t1, 1
        j loopi
    loopi_end:
.end_macro
.data
    array: .space 4050
    
.text
    read_int($s0)
    addi $s1, $s0, -1
    li $t1, 0
    loop1:
        bge $t1, $s0, loop1_end
        read_int($t2)
        mul $t3, $t1, 4
        sw $t2, array($t3)
        addi $t1, $t1, 1
        j loop1
    loop1_end:
    bubble_sort(array, $s1)
    li $t1, 91
    print_char($t1)
    li $t1, 0
    lw $t3, array($t1)
    print_int($t3)
    addi $t1, $t1, 1
    loop2:
        bge $t1, $s0, loop2_end
        mul $t2, $t1, 4
        lw $t3, array($t2)
        dot()
        print_int($t3)
        addi $t1, $t1, 1
        j loop2
    loop2_end:
    li $t1, 93
    print_char($t1)
    exit()
    
    
