.data
num: .word 4

.text
    
    main:
        LI $s0, 0x10010000
        STORE $s2, 0($s0)
        ADD $s1,$s1,$s1