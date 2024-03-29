import globals
from utility_functions import *

from operations import add, sub, bne, load, load_int, store, jump, syscall,move,beq,addi,subi,slt,sb,lb


globals.initialize()

if __name__ == "__main__":
    data_num = 0
    instr_num = 0
    instr_type = "data"
    with open('Test_Programs/bubblesort.s', 'r') as file:
        for instr in file:
            instr = clean_instruction(instr, instr_num)

            if (instr == ".data"):
                instr_type = "data"
            elif (instr == ".text"):
                instr_type = "text"

            if (instr != "" and instr != ".data" and instr != ".text"):
                if (instr_type == "data"):
                    data_num = edit_data(instr, data_num)
                elif(instr_type == "text"):
                    instr = find_label(instr, instr_num)
                    instr = clean_instruction(instr, instr_num)
                    if (instr != ""):
                        globals.instructions.append(instr)
                        instr_num += 1

    '''
    Instructions would be
    add, sub, load, load_int, store, bne, jump
    '''

    pc = 0
    while True:
        instruction = globals.instructions[pc].split()[0]
        if instruction == "add":
            pc = add(pc, globals.instructions[pc])
        elif instruction == "sub":
            pc = sub(pc, globals.instructions[pc])
        elif instruction == "load" or instruction == "lw":
            pc = load(pc, globals.instructions[pc])
        elif instruction == "load_int" or instruction == "li":
            pc = load_int(pc, globals.instructions[pc])
        elif instruction == "store" or instruction == "sw":
            pc = store(pc, globals.instructions[pc])
        elif instruction == "jump" or instruction == "j":
            pc = jump(pc, globals.instructions[pc])
        elif instruction == "bne":
            pc = bne(pc, globals.instructions[pc])
        elif instruction == "beq":
            pc = beq(pc,globals.instructions[pc])
        elif instruction == "move":
            pc = move(pc,globals.instructions[pc])
        elif instruction == "addi":
            pc = addi(pc,globals.instructions[pc])
        elif instruction == "subi":
            pc = subi(pc,globals.instructions[pc])
        elif instruction == "slt":
            pc = slt(pc,globals.instructions[pc])
        elif instruction == "sb":
            pc = sb(pc,globals.instructions[pc])
        elif instruction == "lb":
            pc = lb(pc,globals.instructions[pc])
        elif instruction == "syscall":
            pc = syscall(pc)

