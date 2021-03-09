import globals
from utility_functions import *
from operations import add, sub, bne, load, load_int, store, jump, syscall


globals.initialize()

if __name__ == "__main__":
    data_num = 0
    instr_num = 0
    instr_type = "data"
    with open('test.s', 'r') as file:
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

    pc = 1
    while True:
        instruction = globals.instructions[pc].split()[0]
        if instruction == "add":
            pc = add(pc, globals.instructions[pc])
        elif instruction == "sub":
            pc = sub(pc, globals.instructions[pc])
        elif instruction == "load" or instruction == "lw":
            # print("fetch")
            # print(instruction)
            pc = load(pc, globals.instructions[pc])
        elif instruction == "load_int" or instruction == "li":
            pc = load_int(pc, globals.instructions[pc])
        elif instruction == "store" or instruction == "sw":
            pc = store(pc, globals.instructions[pc])
        elif instruction == "jump":
            pc = jump(pc, globals.instructions[pc])
        elif instruction == "bne":
            pc = bne(pc, globals.instructions[pc])
        # elif instruction == "jr":
        #     jump_register(pc)
        elif instruction == "syscall":
            pc = syscall(pc)
