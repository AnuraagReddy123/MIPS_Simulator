
	.text
main:
	LI $t7, 0x00000001
	LI $t0, 0x0000000a
 	LI $t1, 0x00000000
loop:

 	ADD  $t1, $t1, $t7
 	BNE   $t1, $t0, loop