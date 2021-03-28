from utility_func import fetch_imm, fetch_reg, op_type
import sim_glob


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
            pass #Will do later branch instructions

    sim_glob.queue.append(next_instruction)


def EX(PC, clock, depen_reg = None): # Depen reg just for store
    pass


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
