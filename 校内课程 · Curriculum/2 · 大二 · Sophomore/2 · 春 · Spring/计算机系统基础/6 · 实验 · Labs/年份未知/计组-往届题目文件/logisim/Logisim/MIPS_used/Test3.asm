# initiate
ori $t0, $0, 0         # $t0 = 0x00000000  
ori $t1, $0, 1         # $t1 = 0x00000001  
lui $t2, 0xFFFF         
ori $t2, $t2, 0xFFFF   # $t2 = 0xFFFFFFFF  
lui $t3, 0x7FFF       
ori $t3, $t3, 0xFFFF   # $t3 = 0x7FFFFFFF  
lui $t4, 0x7FFF          
ori $t4, $t4, 0xFFFE   # $t4 = 0x7FFFFFFE  
lui $t5, 0x8000        # $t5 = 0x80000000  
lui $t6, 0x8000          
ori $t6, $t6, 0x0001   # $t6 = 0x80000001   
ori $t7, $t7, 0xFFFF   # $t7 = 0x0000FFFF  
lui $t8, 0x0000    
ori $t8, $t8, 0xFFFE   # $t8 = 0x0000FFFE  
  
sw $t0, 0($0)  
sw $t1, 4($0)  
 
ori $t9, $0, 12  
sw $t2, 0($t9)  
 
ori $a1, $0, 16   
sw $t3, -4($a1)     
  
sub $t7, $0, $a1
sw $t4, 20($t7)         
 
sw $t6, 12($0)   

lw $t6, 0($0)  
lw $t5, 4($0)  
lw $t4, 0($t9) 
lw $t3, -4($t9)   
 
sub $9, $0, $t9    
lw $t1, 16($t9)    
 
add $9, $0, $t9  
lw $0, -8($9)   
