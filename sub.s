    .data
num: .word 5
    
    .text
    .globl main
main:
    li $t0, 45
    sw $t0, num

    li $t1, 10
    li $t2, 45
    bne $t0, $t2, loop
    jump exit
loop:
    add $t0, $t0, $t1
    bne $t0, $t2, loop

exit:
    jr $ra