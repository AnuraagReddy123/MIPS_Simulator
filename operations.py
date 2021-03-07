import globals

base_pc = int("400000",16)

def add(PC, code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find('$') #find first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually 
    # perform the subtraction operation on the registers and get the answer in decimal
    temp_ans = int(globals.registers[fetched_registers[1]],16) + int(globals.registers[fetched_registers[2]],16)
    hex_ans = hex(temp_ans) #convert the integer back into hex form
    # store the hex back into registers and get rid of 0x in the beginning
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:0]
    return PC+1

def sub(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find('$') #find first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually 
    # perform the subtraction operation on the registers and get the answer in decimal
    temp_ans = int(globals.registers[fetched_registers[1]],16) - int(globals.registers[fetched_registers[2]],16)
    hex_ans = hex(temp_ans) #convert the integer back into hex form
     # store the hex back into registers and get rid of 0x in the beginning
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:0]
    return PC+1


def jump(label):
    pc = globals.label_dict[label]
    return pc

def bne(PC,code):# for branch not equal instruction
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    first_register = fetched_registers[0] # get the first register
    second_register = fetched_registers[1] # get the second register
    jump_target = fetched_registers[2] # the jump target
    if globals.registers[first_register] == globals.registers[second_register]: # if the contents are equal
       PC = PC+1
    else:
       PC = globals.label_dict[jump_target] # assign the PC
    return PC

def load(PC, code):
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    # get the word to be stored in the register
    #print("fetched")
    #print(reg_code)
    #print(fetched_registers)
    if fetched_registers[1].find('(') == -1: # if variable name is given instead of address
        word = globals.data_segment[globals.data_dict[fetched_registers[1]]]
        globals.registers[fetched_registers[0]] = word 
    else:
        jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
        address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
        #print(globals.registers[address_register])
        dest_index = int(globals.registers[address_register],16) + jump - globals.base_address
        #print(globals.registers[address_register])
        dest_index = dest_index // 4 # get the destination index
        #print("reached")
        word = globals.data_segment[dest_index]
        #print(fetched_registers[0])
        globals.registers[fetched_registers[0]] = word
        #print(globals.registers[address_register])
    return PC+1

def load_int(PC, code):
    code = code.replace(" ", "")
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    #Check whether int is in decimal or hex
    if fetched_registers[1].find("0x") == -1:
        hex_num = hex(int(fetched_registers[1]))
    else:
        hex_num = fetched_registers[1]
    globals.registers[fetched_registers[0]] = hex_num[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    return PC+1

def store(PC,code): # for store word instruction
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    word = globals.registers[fetched_registers[0]] # get the word to be stored
    if fetched_registers[1].find('(') == -1: # if variable name is given instead of address
        target_name = fetched_registers[1]
        globals.data_segment[globals.data_dict[target_name]] = word 
    else:
        jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
        address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
        dest_index = int(globals.registers[address_register],16) + jump - globals.base_address
        dest_index = dest_index // 4 # get the destination index
        globals.data_segment[dest_index] = word
    return PC+1 # PC for next instruction

def store_data(data_num, data):
    for i in range(0, len(data)):
        #check whether value is hex or not
        if data[i].find("0x")==-1:
            hex_num = hex(int(data[i]))
        else:
            hex_num = data[i]
        globals.data_segment[i+data_num] = hex_num[2:]
        globals.data_segment[i+data_num] = globals.data_segment[i+data_num].rjust(8, '0')
    return data_num+len(data)

def jump_register(PC):
    print(globals.registers)
    print(globals.data_segment)
    print(hex(PC+base_pc).rjust(8,'0'))
    print("reached")
    exit(0) # exit the program 