# Program to test our simulator
.text
    
    main:
        LI $v0, 0x00000000 # load the address of the first word 
        LI $t0, 0x00000000
        LI $t0, 0x00000001
        LI $t0, 0x00000003
    
    loop:
        BEQ $t0, $t2, exit
        ADD $t0, $t0, $t1
        ADD $v0, $t1, $t2
        JUMP loop

    exit:
        ADD $t0, $t, $t1