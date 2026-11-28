 
    # Initialize $t0 with the address of label1  
    
    ori $t0, $t0, 0x3010   # Load lower immediate  

    # Test jal instruction  
    jal function           # Jump and link to function  

    ori $t1, $t0, 0x2443 

    # Test j instruction  
    j label2               # Unconditional jump to label2  

label1:  
    ori $t1, $t0, 0x1887

    # Return from label1  
    jr $ra                 # Jump register to return address  

label2:  
     ori $t1, $t0, 0x3289
 	j end

function:  
    # Test jr instruction  
    jr $t0                 # Jump to the address in $t0 (label1)  
    nop                    # Delay slot
    
end:
