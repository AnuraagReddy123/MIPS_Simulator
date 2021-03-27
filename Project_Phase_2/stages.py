import sim_glob
from utility_func import *


def IF(PC, Prev_PC, clock):  # instruction fetch in python
    # store the fetched instruction
    sim_glob.fetched_instr = sim_glob.instructions[PC]
    clock = clock + 1
    Prev_PC = PC
    PC = PC + 1
    next_instruction = {'ID/RF': [PC, Prev_PC, clock]}
    sim_glob.queue.append(next_instruction)


def IDRF(clock):
    '''
    check for dependency with prev instr
    if yes:
        check if dep_reg value present in final_reg_value
        if yes:
            enqueue ex(decoded_instr, dependent_reg, clk+1)
        else:
            stall
            enqueue idrf(fetched_string, clk+1)
    else:
        enqueu ex(decoded_instr, dependent_reg, clk+1)
    '''
    # If it is not empty
    if bool(sim_glob.curr_decoded_instr):
        # Stall
        next_instruction = {'ID/RF': [clock+1]}
        sim_glob.queue.append(next_instruction)
    else:
        # Decode instr
        instr = sim_glob.fetched_instr
        sim_glob.fetched_instr = ""
        
        # Check dependency with prev_decoded_instr (EX will move curr_decoded_instr to prev_decoded_instr)

        
def EX():
    pass

def MEM():
    pass

def WB():
    pass

    
