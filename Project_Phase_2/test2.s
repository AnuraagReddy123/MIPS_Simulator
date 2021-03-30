.text

 main:
    LI $v0,0x00000000
    LI $t0,0x00000000 
    LI $t1,0x00000001
    LI $t2,0x00000003
loop:
    BEQ $t0,$t2,exit
    ADD $t0,$t0,$t1
    ADD $v0,$t1, $t2
    JUMP loop  

exit:
    ADD $t0, $t0, $t1
