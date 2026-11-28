
lui $t0, 0x0001      
ori $t0, $t0, 0x0001  

lui $t1, 0x0002       
ori $t1, $t1, 0x0002 

lui $t2, 0x0003 
ori $t2, $t2, 0x0003 

lui $t3, 0x0001 
ori $t3, $t3, 0x0001 

lui $t4, 0x0003 
ori $t4, $t4, 0x0003 

abc:
beq $t0, $t1, end
beq $t0, $t2, abc
def:
beq $t1, $t2, def
beq $t0, $t3, jump_forward
jump_backward:
beq $t1, $t3, jump_forward2

jump_forward:
lui $t1, 0x0001  
ori $t1, $t1, 0x0001
beq $t1, $t0, jump_backward


jump_forward2:
lui $t5, 0x0034  
ori $t5, $t5, 0x0034

beq $t2, $t4, jump_next
jump_next:
jump_this:
beq $t2, $t4, jump_this

end:
