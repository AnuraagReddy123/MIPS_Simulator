    .data
num: .word 5
    
    .text
    .globl main
main:
    li $v0, 5
    syscall
    sw $a0, num

    li $v0, 10
    syscall