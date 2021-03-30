# Program to test our simulator

.data
num1: .word 7 
num2: .word 7

.text

    main:
        LI $s0, 0x10010001 # load the address of the first word 
        LOAD $s1, 0($s0) # load the word
        LOAD $s2, 4($s0) # load the second word
        SUB $s3,$s2,$s2 # sub the numbers
