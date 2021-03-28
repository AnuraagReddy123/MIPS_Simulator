from utility_func import fetch_imm, fetch_label, fetch_reg, op_type
import sim_glob
from operations import *


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
    else:
        # Enqueue the same instruction
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
                            sim_glob.fetched_instr = instr
                            sim_glob.decoded_instr = {}
                            break

                    elif reg[2] == sim_glob.que_reg[i].regi and flag_src2 == 0:
                        flag_src2 = 1
                        if sim_glob.que_reg[i].val != None:
                            sim_glob.decoded_instr["src"][reg[2]] = sim_glob.que_reg[i].val
                        else:  # There would be a stall
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

        elif sim_glob.op_dict[op] >= 4:
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
                        if beq(sim_glob.decoded_instr[reg[1]], sim_glob.decoded_instr[reg[2]]) == 1:
                            # Now get the IF from the queue
                            sim_glob.queue[0]["IF"][0] = sim_glob.label_dict[label]    # Update the new PC of the IF instruction
                            sim_glob.queue[0]["IF"][1] += 1        # Increase the clock by 1
                        else:
                            pass # Nothing happens
                    elif op == "BNE":
                        if bne(sim_glob.decoded_instr[reg[1]], sim_glob.decoded_instr[reg[2]]) == 1:
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
                sim_glob.result_of_execution["dest"][dest[0]] = add(src[0], src[1])     # Sum of source registers
            elif op == "SUB":
                sim_glob.result_of_execution["dest"][dest[0]] = sub(src[0], src[1])     # Difference of source registers
            
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

        elif sim_glob.op_dict[op] >=4:
            next_instruction = {"MEM": [PC, clock+1]}
            pass
    
    sim_glob.queue.append(next_instruction)


def MEM(instruction_type, src_registers, dest_registers, clock):
    if instruction_type == 2:  # load instruction
        src_register = next(iter(src_registers))  # get the source register
        # get the destination register
        dest_register = next(iter(dest_registers))
        # fetch the memory address in the memory segment
        memory_address = src_registers[src_register]
        dest_index = int(memory_address, 16) - sim_glob.base_address
        dest_index = dest_index // 4  # get the destination index
        word = sim_glob.data_segment[dest_index]
        sim_glob.mem_result[src_register] = word  # update the dic_mem
        next_instruction = {'WB': [dest_register, word, clock+1]}
    elif instruction_type == 3:  # store instruction
        src_register = next(iter(src_registers))  # get the source register
        # get the destination register
        dest_register = next(iter(dest_registers))
        # fetch the memory address in the memory segment
        memory_address = src_registers[src_register]
        dest_index = int(memory_address, 16) - sim_glob.base_address
        dest_index = dest_index // 4  # get the destination index
        word = dest_registers[dest_register]
        sim_glob.data_segment[dest_index] = word
        next_instruction = {'WB': [dest_register, word, clock+1]}
    else:  # any other instruction
        next_instruction = {'WB': [dest_register, word, clock+1]}
    sim_glob.queue.append(next_instruction)
    pass


def WB():
    pass
