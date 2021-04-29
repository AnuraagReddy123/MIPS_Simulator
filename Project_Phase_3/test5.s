    .text
main:
    LI $s0, 0x10010000
    LOAD $s1, 0($s0)
    LOAD $s1, 8($s0)
    LOAD $s1, 12($s0)
    LOAD $s1, 0($s0)
    LOAD $s1, 8($s0)
    LOAD $s1, 12($s0)
    LOAD $s1, 0($s0)
    LOAD $s1, 8($s0)
    LOAD $s1, 12($s0)

#   IF(1)  ID(2)  EX(3)  MEM(4)   WB(5)
#          IF(2)  ID(3)  EX(4)    MEM(5)                        MEM(104)   WB(105)
#                 IF(3)  ID(4)    EX(5)                                    MEM(105)    MEM(204)    WB(205)