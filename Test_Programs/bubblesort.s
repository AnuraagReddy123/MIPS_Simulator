.data
n: .word 10
	.text
main:
	li $s7, 0x10010000				# load address of numbers into $s7

	li $s0, 0						# initialize counter 1 for loop 1
	lw $s6, n						# n
input: 
	li $v0, 5
	syscall
	addi $s7,$s7,4
	sw $a0, 0($s7)
	subi $s6, $s6, 1
	bne $zero, $s6,input

	li $s7,0x10010004
	lw $s6, n						# n
	subi $s6,$s6,1
	li $s1, 0 						# initialize counter 2 for loop 2

	li $t3, 0						# initialize counter for printing
	li $t4, 10

loop:
	add $t7, $s1, $s1				# multiply $s1 by 2 and put it in t7
	add $t7, $t7, $t7
	add $t7, $s7, $t7 				# add the address of numbers to t7

	lw $t0, 0($t7)  				# load numbers[j]	
	lw $t1, 4($t7) 					# load numbers[j+1]

	slt $t2, $t0, $t1				# if t0 < t1
	bne $t2, $zero, increment

	sw $t1, 0($t7) 					# swap
	sw $t0, 4($t7)

increment:	

	addi $s1, $s1, 1				# increment t1
	sub $s5, $s6, $s0 				# subtract s0 from s6

	bne  $s1, $s5, loop				# if s1 (counter for second loop) does not equal 9, loop
	addi $s0, $s0, 1 				# otherwise add 1 to s0
	li $s1, 0 						# reset s1 to 0

	bne  $s0, $s6, loop				# go back through loop with s1 = s1 + 1
	
print:
	beq $t3, $t4, final				# if t3 = t4 go to final
	
	lw $t5, 0($s7)					# load from numbers
	
	li $v0, 1						# print the number
	move $a0, $t5
	syscall
	
	addi $s7, $s7, 4				# increment through the numbers
	addi $t3, $t3, 1				# increment counter

	j print

final:	
	li $v0, 10						# end program
	syscall