.data
num: .word 4

# Program to test our simulator

.data

num: .word 5

.text
    
    main:
        LI $s0, 0x10010000
        STORE $s2, 0($s0)
        LOAD $s1,0($s0)
        JUMP exit
        SUB $s1,$s2,$s3
    exit:
        ADD $s1,$s1,$s1 