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

.data
    
    
.text
    
    
    
    
    
