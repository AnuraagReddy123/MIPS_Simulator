# program to take test the simulator

    .data

value: .word 0x00000001, 0x00000005

    .text # assembler directive for text segment

    .globl main
    main:
        li $s0, 0x10010000 # load the address of the first integer
        lw $t1, 0($s0) # load the integer 
        lw $t2, 4($s0) # load the second integer
        sub $t3, $t1, $t2 # add the numbers
        sw $t3, 8($s0)
        jr $ra # Exit  