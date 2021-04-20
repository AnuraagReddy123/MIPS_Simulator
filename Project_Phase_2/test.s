.data
num: .word 4

.text
    
    main:
        LI $s0, 0x10010000
        ADD $s1,$s2,$s2
        SUB $s1,$s1,$s2
