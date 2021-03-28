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

def MEM(instruction_type,src_registers,dest_registers,clock):
    dest_register = next(iter(dest_registers)) # get the destination register
    if instruction_type == 2:# load instruction
        src_register = next(iter(src_registers)) # get the source register
        memory_address = src_registers[src_register]# fetch the memory address in the memory segment
        dest_index = int(memory_address,16)  - sim_glob.base_address
        dest_index = dest_index // 4 # get the destination index
        word = sim_glob.data_segment[dest_index]
        sim_glob.dic_mem[src_register] = word # update the dic_mem
        next_instruction = {'WB': [instruction_type,dest_register,word,clock+1]}
    elif instruction_type == 3:# store instruction
        src_register = next(iter(src_registers)) # get the source register
        memory_address = src_registers[src_register]# fetch the memory address in the memory segment
        dest_index = int(memory_address,16)  - sim_glob.base_address
        dest_index = dest_index // 4 # get the destination index
        word = dest_registers[dest_register]
        sim_glob.data_segment[dest_index] = word
        next_instruction = {'WB': [instruction_type,dest_register,word,clock+1]}
    else:# any other instruction
        next_instruction = {'WB': [instruction_type,dest_registers[dest_register],clock+1]}
    sim_glob.queue.append(next_instruction)
    pass

def WB(instruction_type,dest_register,value,clock):
    if instruction_type == 0:# add type instruction
        dest_register = value
    elif instruction_type == 1:# subtract type instruction
        dest_register = value
    elif instruction_type == 2:# load type instruction
        dest_register = value
    sim_glob.latest_clock = clock+1
    pass