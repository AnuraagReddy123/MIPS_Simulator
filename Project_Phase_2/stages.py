import sim_glob

def IF(PC,clock):# instruction fetch in python
    if not sim_glob.fetched_instr: # if no instruction fetch was going on
        sim_glob.fetched_instr = sim_glob.instructions[PC] #store the fetched instruction 
        clock = clock + 1
        next_instruction = {'IDRF' : clock} # Enqueue the next stage
    else:
        next_instruction = {'IF' : [PC,clock+1]}# Enqueue the same instruction
    sim_glob.queue.append(next_instruction)

def IDRF():
    pass

def EX():
    pass

def MEM(instruction_type,src_registers,dest_registers,dependent_register,clock):
    if instruction_type == 2:
        if not dependent_register:
                        
    pass

def WB():
    pass
    

    