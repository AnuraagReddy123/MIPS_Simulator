from sim_glob import *

def IF(PC,Prev_PC,clock):# instruction fetch in python
    globals.fetched_instr = instructions[PC] #store the fetched instruction 
    clock = clock + 1
    Prev_PC = PC
    PC = PC + 1
    next_instruction = {'ID/RF' : [PC,Prev_PC,clock]}
    queue.append(next_instruction)


def WB():
    