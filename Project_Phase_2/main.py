import sim_glob
from utility_func import *
from stages import *

from op import *


sim_glob.initialize()

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
                        sim_glob.instructions.append(instr)
                        instr_num += 1

    '''
    Instructions would be
    add, sub, load, load_int, store, bne, jump
    '''
    sim_glob.queue.append({'IF' : [0,0]})
    pc = 0
    while sim_glob.queue:
        instruction = sim_glob.queue.pop(0)
        stage = next(iter(instruction))
        if stage == 'IF':
            IF(instruction[stage][0],instruction[stage][1])
        elif stage == 'IDRF':
            IDRF(instruction[stage][0],instruction[stage][1])
        elif stage == 'EX':
            EX(instruction[stage][0],instruction[stage][1])
        elif stage == 'MEM':
            MEM(instruction[stage][0],instruction[stage][1])
        else:
            WB(instruction[stage][0],instruction[stage][1])    
