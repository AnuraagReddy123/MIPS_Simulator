.data
num: .word 4

# Program to test our simulator
.text
    
    main:
        LI $v0, 0x00000000 # load the address of the first word 
        LI $t0, 0x00000000
        LI $t1, 0x00000001
        LI $t2, 0x00000003
        LI $t3, 0x10010000
        LOAD $t4, 0($t3)
    
    loop:
        BEQ $t0, $t2, exit
        ADD $t0, $t0, $t1
        ADD $v0, $t1, $t2
        JUMP loop

    exit:
        ADD $t0, $t0, $t1
