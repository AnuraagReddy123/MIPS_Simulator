    .text
main:
    LI $s0, 0x10010000
    LOAD $s1, 0($s0)
    LOAD $s1, 4($s0)
    