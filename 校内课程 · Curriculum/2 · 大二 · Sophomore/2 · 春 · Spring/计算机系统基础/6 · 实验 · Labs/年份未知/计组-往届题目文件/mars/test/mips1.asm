.data
	enter: .asciiz "\n"
	
.text
	li $v0, 4
	la $a0, enter	
	syscal