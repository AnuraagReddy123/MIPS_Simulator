import sim_glob
from utility_func import *
from stages import *
from collections import OrderedDict
from op import *
import cache


sim_glob.initialize()

if __name__ == "__main__":

    # Read cache parameters
    with open('cache_param.txt', 'r') as file:
        blockSize = int(file.readline())
        assoc = int(file.readline())
        cacheSize = int(file.readline())
        sim_glob.accessL1 = int(file.readline())
        sim_glob.L1_cache = cache.Cache(blockSize, assoc, cacheSize)
        blockSize = int(file.readline())
        assoc = int(file.readline())
        cacheSize = int(file.readline())
        sim_glob.accessL2 = int(file.readline())
        sim_glob.L2_cache = cache.Cache(blockSize, assoc, cacheSize)
        sim_glob.accessMemory = int(file.readline())

    data_num = 0
    instr_num = 0
    instr_type = "data"
    with open('test.s', 'r') as file:
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


    forwarding = str(input("Enter yes if forwarding needs to be enabled else enter no: ")).lower()
    if forwarding == "yes":
        sim_glob.data_forwarding = True
    else:
        sim_glob.data_forwarding = False
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
    number_of_stalls = len(sim_glob.stalled_instructions)
    sim_glob.latest_clock += sim_glob.memoryStallCycles
    print(f"Number of cycles: {sim_glob.latest_clock}")
    print(f"Number of stalls: {number_of_stalls}")
    number_of_instructions = len(sim_glob.instructions)
    IPC = number_of_instructions / sim_glob.latest_clock
    print(f"IPC of the pipeline: {IPC:.3f}")
    # remove the duplicated instructions 
    sim_glob.stalled_instructions = list(OrderedDict.fromkeys(sim_glob.stalled_instructions))
    print(f"List of stalled instructions due to pipeline {sim_glob.stalled_instructions}")
    # print(sim_glob.data_segment) uncomment this line to print the data segment
    print(sim_glob.registers)
    firstLevelMissRate = 0
    secondLevelMissRate = 0
    if sim_glob.L1_cache.numberOfAccesses:
        firstLevelMissRate = sim_glob.L1_cache.numberOfMisses / sim_glob.L1_cache.numberOfAccesses # miss rate of L1
    if sim_glob.L2_cache.numberOfAccesses:
        secondLevelMissRate = sim_glob.L2_cache.numberOfMisses / sim_glob.L2_cache.numberOfAccesses # miss rate of L2
    print(f"Miss rate of L1 cache: {firstLevelMissRate: .3f}")
    print(f"Miss rate of L2 cache: {secondLevelMissRate: .3f}")