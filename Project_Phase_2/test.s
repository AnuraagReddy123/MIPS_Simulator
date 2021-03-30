.data
num: .word 4

.text
    
    main:
        LI $s0, 0x10010000
        LOAD $s1, 0($s0)
        ADD $s1,$s1,$s1
        JUMP main