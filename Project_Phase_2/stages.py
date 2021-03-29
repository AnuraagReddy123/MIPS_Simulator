from utility_func import fetch_imm, fetch_label, fetch_reg, op_type
import sim_glob
from op import *


class DepReg:
    def __init__(self, regi, pc, val):
        self.regi = regi
        self.pc = pc
        self.val = val


def IF(PC, clock):  # instruction fetch in python
    if not sim_glob.fetched_instr:  # if no instruction fetch was going on
        # store the fetched instruction
        sim_glob.fetched_instr = sim_glob.instructions[PC]
        clock = clock + 1
        next_instruction = {'IDRF': [PC, clock]}  # Enqueue the next stage
        sim_glob.queue.append(next_instruction)
        if PC < len(sim_glob.instructions):# if we are not done with all instructions yet
            next_next_instrucution = {'IF' : [PC+1,clock]} # enqueue the next instruction
            sim_glob.queue.append(next_next_instrucution)
    else:
        # Enqueue the same instruction
        sim_glob.stalled_instructions.append(sim_glob.instructions[PC])
        next_instruction = {'IF': [PC, clock+1]}
        sim_glob.queue.append(next_instruction)


def IDRF(PC, clock):
    # If it is not empty
    next_instruction = {}
    if bool(sim_glob.decoded_instr):
        # Stall
        next_instruction = {'ID/RF': [PC, clock+1]}

    else:
        # Decode instr
        instr = sim_glob.fetched_instr
        sim_glob.fetched_instr = ""

        op = op_type(instr)
        sim_glob.decoded_instr["op"] = op  # Put operation in dictionary

        # Fetch register and value
        if sim_glob.op_dict[op] < 2:  # Add type instr
            reg = fetch_reg(instr)
            flag_src1 = 0
            flag_src2 = 0
            # Checking dependencies
            if len(sim_glob.que_reg) != 0:
                sim_glob.decoded_instr["dest"][reg[0]] = None
                for i in range(len(sim_glob.que_reg)-1, -1, -1):  # Go through loop backwards
                    if reg[1] == sim_glob.que_reg[i].regi and flag_src1 == 0:
                        flag_src1 = 1
                        # The register is not empty
                        if sim_glob.que_reg[i].val != None:
                            sim_glob.decoded_instr["src"][reg[1]] = sim_glob.que_reg[i].val
                        else:  # There would be a stall
                            next_instruction = {"ID/RF": [PC, clock+1]}
                            sim_glob.stalled_instructions.append(instr)
                            sim_glob.fetched_instr = instr
                            sim_glob.decoded_instr = {}
                            break

                    elif reg[2] == sim_glob.que_reg[i].regi and flag_src2 == 0:
                        flag_src2 = 1
                        if sim_glob.que_reg[i].val != None:
                            sim_glob.decoded_instr["src"][reg[2]] = sim_glob.que_reg[i].val
                        else:  # There would be a stall
                            sim_glob.stalled_instructions.append(instr)
                            next_instruction = {"ID/RF": [PC, clock+1]}
                            sim_glob.fetched_instr = instr
                            sim_glob.decoded_instr = {}
                            break
                else:  # If the for loop didn't break
                    # If flag_src1 and flag_src2 weren't triggered then they weren't dependent registers
                    next_instruction = {"EX": [PC, clock+1]}
                    if flag_src1 == 0:
                        sim_glob.decoded_instr["src"][reg[1]] = sim_glob.registers[reg[1]]
                    if flag_src2 == 0:
                        sim_glob.decoded_instr["src"][reg[2]] = sim_glob.registers[reg[2]]
                    # Since the destination register is not calculated yet
                    sim_glob.que_reg.append(DepReg(reg[0], PC, None))

            else:  # There are no dependencies
                sim_glob.decoded_instr["dest"][reg[0]] = None
                sim_glob.decoded_instr["src"][reg[1]] = sim_glob.registers[reg[1]]
                sim_glob.decoded_instr["src"][reg[2]] = sim_glob.registers[reg[2]]
                next_instruction = {"EX": [PC, clock+1]}
                sim_glob.que_reg.append(DepReg(reg[0], PC, None))

        elif sim_glob.op_dict[op] >= 2 and sim_glob.op_dict[op] < 4: # Load type instr
            reg = fetch_reg(instr)
            # Check dependency
            flag_src1 = 0
            
            if len(sim_glob.que_reg) != 0:
                sim_glob.decoded_instr["dest"][reg[0]] = sim_glob.registers[reg[0]]
                sim_glob.decoded_instr["imm"] = fetch_imm(instr)
                for i in range(len(sim_glob.que_reg)-1, -1, -1):  # Go through loop backwards
                    if reg[1] == sim_glob.que_reg[i].regi and flag_src1 == 0:
                        flag_src1 = 1
                        # The register is not empty
                        if sim_glob.que_reg[i].val != None:
                            sim_glob.decoded_instr["src"][reg[1]] = sim_glob.que_reg[i].val
                        else:  # There would be a stall
                            sim_glob.stalled_instructions.append(instr)
                            next_instruction = {"ID/RF": [PC, clock+1]}
                            sim_glob.fetched_instr = instr
                            sim_glob.decoded_instr = {}
                            break
                else:  # If the for loop didn't break
                    # If flag_src1 wasn't triggered then they weren't dependent registers
                    if flag_src1 == 0:
                        sim_glob.decoded_instr["src"][reg[1]] = sim_glob.registers[reg[1]]
                    next_instruction = {"EX": [PC, clock+1]}
                    # Since the destination register is not calculated yet
                    if op == "LOAD":
                        sim_glob.que_reg.append(DepReg(reg[0], PC, None))

            else:  # There are no dependencies
                sim_glob.decoded_instr["dest"][reg[0]] = sim_glob.registers[reg[0]]
                sim_glob.decoded_instr["imm"] = fetch_imm(instr)
                sim_glob.decoded_instr["src"][reg[1]] = sim_glob.registers[reg[1]]
                next_instruction = {"EX": [PC, clock+1]}
                sim_glob.que_reg.append(DepReg(reg[0], PC, None))

        elif sim_glob.op_dict[op] >= 4 and sim_glob.op_dict[op] < 6:
            if op == "BEQ" or op == "BNE":
                reg = fetch_reg(instr)
                label = fetch_label(instr)
                flag_src1 = 0
                flag_src2 = 0
                flag_break = 0
                #Check dependency
                if len(sim_glob.que_reg) != 0:
                    for i in range(len(sim_glob.que_reg)-1, -1, -1):  # Go through loop backwards
                        if reg[0] == sim_glob.que_reg[i].regi and flag_src1 == 0:
                            flag_src1 = 1
                            # The register is not empty
                            if sim_glob.que_reg[i].val != None:
                                sim_glob.decoded_instr[reg[0]] = sim_glob.que_reg[i].val
                            else:  # There would be a stall
                                sim_glob.stalled_instructions.append(instr)
                                next_instruction = {"ID/RF": [PC, clock+1]}
                                sim_glob.fetched_instr = instr
                                sim_glob.decoded_instr = {}
                                flag_break = 1
                                break

                        elif reg[1] == sim_glob.que_reg[i].regi and flag_src2 == 0:
                            flag_src2 = 1
                            if sim_glob.que_reg[i].val != None:
                                sim_glob.decoded_instr[reg[1]] = sim_glob.que_reg[i].val
                            else:  # There would be a stall
                                sim_glob.stalled_instructions.append(instr)
                                next_instruction = {"ID/RF": [PC, clock+1]}
                                sim_glob.fetched_instr = instr
                                sim_glob.decoded_instr = {}
                                flag_break = 1
                                break
                    else:  # If the for loop didn't break
                        # If flag_src1 and flag_src2 weren't triggered then they weren't dependent registers
                        next_instruction = {"EX": [PC, clock+1]}
                        if flag_src1 == 0:
                            sim_glob.decoded_instr[reg[1]] = sim_glob.registers[reg[1]]
                        if flag_src2 == 0:
                            sim_glob.decoded_instr[reg[2]] = sim_glob.registers[reg[2]]

                else:  # There are no dependencies
                    sim_glob.decoded_instr[reg[1]] = sim_glob.registers[reg[1]]
                    sim_glob.decoded_instr[reg[2]] = sim_glob.registers[reg[2]]
                    next_instruction = {"EX": [PC, clock+1]}

                if flag_break == 0:
                    # Now we have the values to compare
                    if op == "BEQ":
                        if BEQ(sim_glob.decoded_instr[reg[1]], sim_glob.decoded_instr[reg[2]]) == 1:
                            # Now get the IF from the queue
                            sim_glob.queue[0]["IF"][0] = sim_glob.label_dict[label]    # Update the new PC of the IF instruction
                            sim_glob.queue[0]["IF"][1] += 1        # Increase the clock by 1
                        else:
                            pass # Nothing happens
                    elif op == "BNE":
                        if BNE(sim_glob.decoded_instr[reg[1]], sim_glob.decoded_instr[reg[2]]) == 1:
                            # Now get the IF from the queue
                            sim_glob.queue[0]["IF"][0] = sim_glob.label_dict[label]    # Update the new PC of the IF instruction
                            sim_glob.queue[0]["IF"][1] += 1        # Increase the clock by 1
                        else:
                            pass # Nothing happens
            elif op == "JUMP":
                label = instr.split()[1]
                sim_glob.queue[0]["IF"][0] = sim_glob.label_dict[label]    # Update the new PC of the IF instruction
                sim_glob.queue[0]["IF"][1] += 1        # Increase the clock by 1
                next_instruction = {"EX": [PC, clock+1]}
        elif sim_glob.op_dict[op] == 6: # for load immediate instruction
            reg = fetch_reg[instr]
            sim_glob.que_reg.append(DepReg(reg[0],PC,None))
            pass
    sim_glob.queue.append(next_instruction)


def EX(PC, clock): # Depen reg just for store
    # If it is not empty
    next_instruction = {}
    if bool(sim_glob.result_of_execution):
        # Stall
        next_instruction = {'EX': [PC, clock+1]}
    else:
        dec_instr = sim_glob.decoded_instr
        sim_glob.result_of_execution = sim_glob.decoded_instr       # This will be passed on to memory
        sim_glob.decoded_instr = {}
        
        op = dec_instr["op"]
        if sim_glob.op_dict[op] < 2:
            src = list(dec_instr["src"].keys())    # To get the source registers from the dictionary
            dest = list(dec_instr["dest"].keys())   # To get the destination register from the dictionary
            if op == "ADD":
                sim_glob.result_of_execution["dest"][dest[0]] = ADD(src[0], src[1])     # Sum of source registers
            elif op == "SUB":
                sim_glob.result_of_execution["dest"][dest[0]] = SUB(src[0], src[1])     # Difference of source registers
            
            #Update value in dependent register
            for i in range(0, len(sim_glob.que_reg)):
                if sim_glob.que_reg[i].regi == dest[0] and sim_glob.que_reg[i].pc == PC:
                    sim_glob.que_reg[i].val = sim_glob.result_of_execution["dest"][dest[0]]

            next_instruction = {"MEM": [PC, clock+1]}

        elif sim_glob.op_dict[op] >=2 and sim_glob.op_dict < 4:
            src = list(dec_instr["src"].keys())
            dest = list(dec_instr["dest"].keys())
            imm = dec_instr["imm"]
            mem_address = add_mem(dec_instr["src"][src[0]], imm)        # Finding the memory address
            sim_glob.result_of_execution["src"] = mem_address   # Changing dictionary value to store memory address in src instead of {r1:5}
            
            #Check dependencies for mem to mem forwarding (ONLY FOR STORE)
            if op == "STORE":
                flag_src1 = 0
                if len(sim_glob.que_reg) != 0:
                    for i in range(len(sim_glob.que_reg)-1, -1, -1):  # Go through loop backwards
                        if dest[0] == sim_glob.que_reg[i].regi and flag_src1 == 0:
                            flag_src1 = 1
                            # The register is not empty
                            if sim_glob.que_reg[i].val != None:
                                sim_glob.decoded_instr["dest"] = sim_glob.que_reg[i].val
                            else:  # There would be a stall
                                next_instruction = {"EX": [PC, clock+1]}
                                sim_glob.decoded_instr = dec_instr
                                sim_glob.result_of_execution = {}
                                break
                    else:  # If the for loop didn't break
                        # If flag_src1 wasn't triggered then they weren't dependent registers
                        if flag_src1 == 0:
                            sim_glob.result_of_execution["dest"]= sim_glob.registers[dest[0]]
                        next_instruction = {"MEM": [PC, clock+1]}

                else:  # There are no dependencies
                    sim_glob.result_of_execution["dest"] = sim_glob.registers[dest[0]]
                    next_instruction = {"EX": [PC, clock+1]} 
            else: # In the case of load destination is empty
                sim_glob.result_of_execution["dest"][dest[0]] = None
                next_instruction = {"EX": [PC, clock+1]}

        elif sim_glob.op_dict[op] == 6: # LI instruction
            value = sim_glob.result_of_execution['src'] # get the word in hex
            for i in range(len(sim_glob.que_reg)): # search the queue to update the value
                if sim_glob.que_reg[i].pc == PC: # if PC is found
                    sim_glob.que_reg[i].val = value # update the word to be updated in WB
                    break
            next_instruction = {"MEM": [PC, clock+1]}
    sim_glob.queue.append(next_instruction)

def MEM(PC,clock):
    instruction_type = sim_glob.result_of_execution['op'] # get the instruction type
    if  instruction_type == 'LOAD':# load instruction
        memory_address = sim_glob.result_of_execution['src']# fetch the memory address in the memory segment
        src_index = int(memory_address,16)  - sim_glob.base_address
        src_index = src_index // 4 # get the destination index
        dest_register = next(iter(sim_glob.result_of_execution['dest'])) # get the destination register 
        word = sim_glob.data_segment[src_index] # get the word
        for i in range(len(sim_glob.que_reg)): # search the queue to update the value
            if sim_glob.que_reg[i].pc == PC: # if PC is found
                sim_glob.que_reg[i].val = word # update the word to be updated in WB
                break
        sim_glob.mem_result.update({dest_register:word}) # update the value for WB
    elif instruction_type == 'STORE':# store instruction
        memory_address = sim_glob.result_of_execution['src']# fetch the memory address in the memory segment
        dest_index = int(memory_address,16)  - sim_glob.base_address
        dest_index = dest_index // 4 # get the destination index
        word = sim_glob.result_of_execution['dest'] # get the word from the register
        sim_glob.data_segment[dest_index] = word # store the word in the memory
    elif instruction_type == 'ADD' or instruction_type == 'SUB':
        dest_register = next(iter(sim_glob.result_of_execution['dest'])) # fetch the destination register
        value = sim_glob.result_of_execution['dest'][dest_register] # get the value to be stored
        for i in range(len(sim_glob.que_reg)): # search the queue to update the value
            if sim_glob.que_reg[i].pc == PC: # if PC is found
                sim_glob.que_reg[i].val = value # update the word to be updated in WB
                break
        sim_glob.mem_result.update({dest_register:value}) # update the value for WB
    elif instruction_type == 'LI':
        dest_register = next(iter(sim_glob.result_of_execution['dest'])) # get the destination register
        value = sim_glob.result_of_execution['src'] # get the value to be loaded
        sim_glob.mem_result.update({dest_register:value}) # update the value for WB
    next_instruction = {'WB': [clock+1]}
    sim_glob.result_of_execution.clear()
    sim_glob.queue.append(next_instruction)

def WB(PC,clock):
    if sim_glob.mem_result: # if dictionary is not empty
        dest_register = next(iter(sim_glob.mem_result))
        value = sim_glob.mem_result[dest_register]
        sim_glob.registers[dest_register] = value # WB to the register 
    sim_glob.mem_result.clear()
    sim_glob.latest_clock = clock+1
    
