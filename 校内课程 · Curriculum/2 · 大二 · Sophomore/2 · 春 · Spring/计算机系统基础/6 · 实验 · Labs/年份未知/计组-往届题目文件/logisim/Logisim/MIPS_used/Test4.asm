# initiate  
ori $t0, $0, 0x0F      # $t0 = 0x0000000F  
ori $t1, $0, 0x03      # $t1 = 0x00000003  
lui $t2, 0xFFFF        
ori $t2, $t2, 0xFFFF   # $t2 = 0xFFFFFFFF  
lui $t3, 0x7FFF        
ori $t3, $t3, 0xFFFF   # $t3 = 0x7FFFFFFF  
lui $t4, 0x8000        
ori $t4, $t4, 0x0001   # $t4 = 0x80000001  
lui $t5, 0x8000        
ori $t5, $t5, 0xFFFE   # $t5 = 0x8000FFFE  
ori $t6, $0, 0xAA      # $t6 = 0x000000AA  
ori $t7, $0, 0x55      # $t7 = 0x00000055  
ori $t8, $0, 0xFF      # $t8 = 0x000000FF  
ori $t9, $0, 0x0C      # $t9 = 0x0000000C  

# 测试 sll 指令  
sll $a0, $t0, 2        # $a0 = $t0 << 2  (结果 = 0x0000003C)  
sll $a1, $t1, 3        # $a1 = $t1 << 3  (结果 = 0x00000018)  
sll $a2, $t2, 14        # $a2 = $t2 << 4  (结果 = 0xFFFFFFFFF0)  
sll $t3, $t3, 25        # $t3 = $t3 << 5  (结果 = 0x3FFFFFFF80)  
sll $t4, $t4, 13        # $t4 = $t4 << 6  (结果 = 0x20000000)  
sll $t5, $t5, 27        # $t5 = $t5 << 7  (结果 = 0x4000FFFE00)  
sll $t6, $t6, 8        # $t6 = $t6 << 8  (结果 = 0xAA000000)  
sll $t7, $t7, 19        # $t7 = $t7 << 9  (结果 = 0x00005500)  
sll $t8, $t8, 30       # $t8 = $t8 << 10 (结果 = 0x0000FC00)  
sll $t9, $t9, 31       # $t9 = $t9 << 11 (结果 = 0x00006000)  

# 测试 and 指令  
and $s0, $t0, $t1      # $s0 = $t0 & $t1  (结果 = 0x00000003)  
and $s1, $t2, $t3      # $s1 = $t2 & $t3  (结果 = 0x7FFFFFFF)  
and $s2, $t4, $t5      # $s2 = $t4 & $t5  (结果 = 0x80000000)  
and $s3, $t6, $t7      # $s3 = $t6 & $t7  (结果 = 0x00000000)  
and $s4, $t8, $t9      # $s4 = $t8 & $t9  (结果 = 0x00000000)  
and $s5, $t0, $t6      # $s5 = $t0 & $t6  (结果 = 0x00000000)  
and $s6, $t1, $t7      # $s6 = $t1 & $t7  (结果 = 0x00000001)  
and $s7, $t2, $t8      # $s7 = $t2 & $t8  (结果 = 0x000000AA)  
and $s0, $t3, $t9      # $s0 = $t3 & $t9  (结果 = 0x0000000C)

ori $t0, $0, 3004
ori $t1, $0, 3008
ori $t2, $0, 3016
ori $t3, $0, 3012
ori $t4, $0, 3000
ori $t5, $0, 3004