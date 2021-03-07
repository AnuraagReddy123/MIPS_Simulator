import globals
from operations import *

globals.initialize()

def find_label (instr, instr_num):
    label_index = instr.find(":")
    if label_index != -1:
        label = instr[:label_index]
        globals.label_dict[label] = instr_num
        instr = instr.replace(instr[:label_index+1], "")
    return instr

def clean_instruction(instr, instr_num):
    instr = instr.strip()
    instr = instr.replace("\n", "")
    
    #Searching for comments
    comment_index = instr.find('#')
    if comment_index != -1:
        globals.comments[instr[comment_index:]] = instr_num
        instr = instr.replace(instr[comment_index:], "")
        instr = instr.strip()
    
    return instr

def edit_data(instr, data_num):
    instr = instr.replace(" ", "")
    variable_index = instr.find(":")
    if variable_index!=-1:
        variable = instr[:variable_index]
        index = instr.find(".word")
        data = instr[index+5:].split(',')       # Putting all the data in a list
        globals.data_dict[variable] = data_num  
        data_num = store_data(data_num, data)   # Placing all data in data segment properly
    return data_num

if __name__ == "__main__":
    data_num = 0
    instr_num = 0
    instr_type = "data"
    with open('test.txt', 'r') as file:
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
                    if (instr!=""):
                        globals.instructions.append(instr)
                        instr_num += 1
    
    print(globals.data_segment)
    print('\n')
    print(globals.data_dict)
    print('\n')
    print(globals.instructions)
    print('\n')
    print(globals.label_dict)

    '''
    Insturctions would be
    add, sub, load, load_int, store, bne, jump
    '''

    pc = 0
    while True:
        instruction = globals.instructions[pc].split()[0]
        if instruction == "add":
            pc = add(pc, globals.instructions[pc])
        elif instruction == "sub":
            pc = sub(pc, globals.instructions[pc])
        elif instruction == "load":
            pc = load(pc, globals.instructions[pc])
        elif instruction == "load_int":
            pc = load_int(pc, globals.instructions[pc])
        elif instruction == "store":
            pc = store(pc, globals.instructions[pc])
        elif instruction == "jump":
            pc = jump(pc, globals.instructions[pc])
        elif instruction == "bne":
            pc = bne(pc, globals.instructions[pc])