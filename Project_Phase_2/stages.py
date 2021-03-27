import sim_glob

def IF(PC,clock):# instruction fetch in python
    if not sim_glob.fetched_instr: # if no instruction fetch was going on
        sim_glob.fetched_instr = sim_glob.instructions[PC] #store the fetched instruction 
        clock = clock + 1
        next_instruction = {'IDRF' : clock} # Enqueue the next stage
    else:
        next_instruction = {'IF' : [PC,clock+1]}# Enqueue the same instruction
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

def MEM(instruction_type,src_registers,dest_registers,dependent_register,clock):
    if instruction_type == 2:
        if not dependent_register:
                        
    pass

def WB():
    pass
    

    
