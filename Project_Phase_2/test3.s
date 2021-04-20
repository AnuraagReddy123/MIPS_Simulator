.data
n: .word 3
numbers: .word 102 ,3 ,1 
	.text
main:
	LI $t7, 0x10010000
	LOAD $t1, 4($t7)
    STORE $t1, 0($t7) 					# swap
	STORE $t0, 4($t7)	