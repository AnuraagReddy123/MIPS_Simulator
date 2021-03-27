from utility_func import fetch_imm, fetch_reg, op_type
import sim_glob


def IF(PC, clock):  # instruction fetch in python
    if not sim_glob.fetched_instr:  # if no instruction fetch was going on
        # store the fetched instruction
        sim_glob.fetched_instr = sim_glob.instructions[PC]
        clock = clock + 1
        next_instruction = {'IDRF': clock}  # Enqueue the next stage
    else:
        # Enqueue the same instruction
        next_instruction = {'IF': [PC, clock+1]}
    sim_glob.queue.append(next_instruction)


def IDRF(clock):
    # If it is not empty
    if bool(sim_glob.decoded_instr):
        # Stall
        next_instruction = {'ID/RF': clock+1}

    else:
        # Decode instr
        instr = sim_glob.fetched_instr
        sim_glob.fetched_instr = ""

        op = op_type(instr)
        sim_glob.decoded_instr["op"] = op  # Put operation in dictionary

        # Fetch register and value
        if sim_glob.op_dict[op] < 2:  # Add type instr
            reg = fetch_reg(instr)

            # Check for dependency
            if reg[1] in sim_glob.dic_mem or reg[2] in sim_glob.dic_mem:
                # Stall occurs
                next_instruction = {"ID/RF": clock+1}
                sim_glob.fetched_instr = instr
                sim_glob.decoded_instr = {}
            else:
                if reg[1] in sim_glob.dic_exe and reg[2] in sim_glob.dic_exe:
                    sim_glob.decoded_instr["dest"] = {
                        reg[0]: sim_glob.registers[reg[0]]}
                    sim_glob.decoded_instr["src"] = {
                        reg[1]: sim_glob.dic_exe[reg[1]], reg[2]: sim_glob.dic_exe[reg[2]]}

                elif reg[1] in sim_glob.dic_exe:
                    sim_glob.decoded_instr["dest"] = {
                        reg[0]: sim_glob.registers[reg[0]]}
                    sim_glob.decoded_instr["src"] = {
                        reg[1]: sim_glob.dic_exe[reg[1]], reg[2]: sim_glob.registers[reg[2]]}
                
                elif reg[2] in sim_glob.dic_exe:
                    sim_glob.decoded_instr["dest"] = {
                        reg[0]: sim_glob.registers[reg[0]]}
                    sim_glob.decoded_instr["src"] = {
                        reg[1]: sim_glob.registers[reg[1]], reg[2]: sim_glob.dic_exe[reg[2]]}
                else:
                    sim_glob.decoded_instr["dest"] = {
                        reg[0]: sim_glob.registers[reg[0]]}
                    sim_glob.decoded_instr["src"] = {
                        reg[1]: sim_glob.registers[reg[1]], reg[2]: sim_glob.registers[reg[2]]}
            
                # Other instruction might be dependent on it
                sim_glob.dic_exe[reg[0]] = None
                


        elif sim_glob.op_dict[op] >= 2 and sim_glob.op_dict[op] < 4:
            pass  # Will do later for branch instr

        elif sim_glob.op_dict[op] >= 4:
            reg = fetch_reg(instr)
            sim_glob.decoded_instr["dest"] = {
                reg[0]: sim_glob.registers[reg[0]]}
            sim_glob.decoded_instr["src"] = {
                reg[1]: sim_glob.registers[reg[1]]}
            sim_glob.decoded_instr["imm"] = fetch_imm(instr)

    sim_glob.queue.append(next_instruction)


def EX():
    pass

def MEM(instruction_type,src_registers,dest_registers,clock):
    if instruction_type == 2:# load instruction
        src_register = next(iter(src_registers)) # get the source register
        dest_register = next(iter(dest_registers)) # get the destination register
        memory_address = src_registers[src_register]# fetch the memory address in the memory segment
        dest_index = int(memory_address,16)  - sim_glob.base_address
        dest_index = dest_index // 4 # get the destination index
        word = sim_glob.data_segment[dest_index]
        sim_glob.mem_result[src_register] = word # update the dic_mem
        next_instruction = {'WB': [dest_register,word,clock+1]}
    elif instruction_type == 3:# store instruction
        src_register = next(iter(src_registers)) # get the source register
        dest_register = next(iter(dest_registers)) # get the destination register
        memory_address = src_registers[src_register]# fetch the memory address in the memory segment
        dest_index = int(memory_address,16)  - sim_glob.base_address
        dest_index = dest_index // 4 # get the destination index
        word = dest_registers[dest_register]
        sim_glob.data_segment[dest_index] = word
        next_instruction = {'WB': [dest_register,word,clock+1]}
    else:# any other instruction
        next_instruction = {'WB': [dest_register,word,clock+1]}
    sim_glob.queue.append(next_instruction)
    pass


def WB():
    pass
