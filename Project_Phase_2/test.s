# Program to test our simulator

.data
num1: .word 5 
num2: .word 6

.text

    main:
        LI $s0, 0x10010001 # load the address of the first word 
        LOAD $s1, 0($s0) # load the word
        LOAD $s2, 4($s0) # load the second word
        ADD $s3,$s1,$s2 # add the numbers