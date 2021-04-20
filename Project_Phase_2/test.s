.data
n: .word 10
numbers: .word 102, 3, 1, 5, 13, 16, 4, 10, 9, 11 
	.text
main:
	LI $s7, 0x10010000				# load address of numbers into $s7

	LI $s0, 0x00000000						# initialize counter 1 for loop 1
	LOAD $s6, 0($s7)						# n
input: 
	LOAD $s6, 0($s7)						# n
	LI $s7,0x10010004
	LI $t7, 0x00000001
	SUB $s6,$s6,$t7
	LI $s1, 0x00000000 						# initialize counter 2 for loop 2

	LI $t3, 0x00000000						# initialize counter for printing
	LI $t4, 0x0000000a

loop:
	ADD $t7, $s1, $s1				# multiply $s1 by 2 and put it in t7
	ADD $t7, $t7, $t7
	ADD $t7, $s7, $t7 				# add the address of numbers to t7

	LOAD $t0, 0($t7)  				# load numbers[j]	
	LOAD $t1, 4($t7) 					# load numbers[j+1]

	SLT $t2, $t0, $t1				# if t0 < t1
	BNE $t2, $ze, increment

	STORE $t1, 0($t7) 					# swap
	STORE $t0, 4($t7)

increment:	
    LI $t5, 0x00000001
	ADD $s1, $s1, $t5				# increment t1
	SUB $s5, $s6, $s0 				# subtract s0 from s6

	BNE  $s1, $s5, loop				# if s1 (counter for second loop) does not equal 9, loop
	ADD $s0, $s0, $t5				# otherwise add 1 to s0
	LI $s1, 0x00000000 						# reset s1 to 0

	BNE  $s0, $s6, loop				# go back through loop with s1 = s1 + 1
