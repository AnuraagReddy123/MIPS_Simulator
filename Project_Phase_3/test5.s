    .text
main:
    LI $t2, 0x10010000
    LOAD $t3, 0($t2)

#   IF(1)  ID(2)  EX(3)  MEM(4)   WB(5)
#          IF(2)  ID(3)  EX(4)    MEM(5)                        MEM(104)   WB(105)
#                 IF(3)  ID(4)    EX(5)                                    MEM(105)    MEM(204)    WB(205)