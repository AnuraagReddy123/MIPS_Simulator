    .text
main:
    LI $t4, 0x00000004
    LOAD $t5, 0($t3)
    LOAD $t5, 0($t4)
    LOAD $t5, 0($t5)
	LOAD $t6, 0($t3)

1  2  3  4  5  6  7  8
IF ID EX ME WB
   IF ID EX ME st WB
      IF ID EX st ME WB 