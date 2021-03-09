import globals
from utility_functions import find_2s_complement

base_pc = int("400000",16)

def add(PC, code):
    #print(code)
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find('$') #find first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually 
    # perform the subtraction operation on the registers and get the answer in decimal
    #print(globals.registers[fetched_registers[1]])
    temp_ans = int(globals.registers[fetched_registers[1]],16) + int(globals.registers[fetched_registers[2]],16)
    hex_ans = hex(temp_ans) #convert the integer back into hex form
    # store the hex back into registers and get rid of 0x in the beginning
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:]
    return PC+1

def addi(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find("$") # find the first occurrence $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    value = 0
    if fetched_registers[2].find("0x") != -1:
        value = int(fetched_registers[2],16)
    else:
        value = int(fetched_registers[2])
    hex_ans = hex(int(globals.registers[fetched_registers[1]],16) + value)
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:]
    return PC+1

def sub(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find('$') #find first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually 
    # perform the subtraction operation on the registers and get the answer in decimal
    temp_ans = int(globals.registers[fetched_registers[1]],16) - int(globals.registers[fetched_registers[2]],16)
    hex_ans = ''
    if (temp_ans < 0):
        hex_ans = find_2s_complement(temp_ans)
    else:
        hex_ans = hex(temp_ans) #convert the integer back into hex form
     # store the hex back into registers and get rid of 0x in the beginning
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:]
    return PC+1


def jump(pc, code):
    code = code.split()
    pc = globals.label_dict[code[1]]
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
    if fetched_registers[1].find('(') == -1: # if variable name is given instead of address
        word = globals.data_segment[globals.data_dict[fetched_registers[1]]]
        globals.registers[fetched_registers[0]] = word 
    else:
        jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
        address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
        dest_index = int(globals.registers[address_register],16) + jump - globals.base_address
        #print(code)
        dest_index = dest_index // 4 # get the destination index
        #print(dest_index)
        word = globals.data_segment[dest_index]
        globals.registers[fetched_registers[0]] = word
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
    #print(hex_num)
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
  
def move(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find("$") # find the first occurrence $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    first_register = fetched_registers[0] # get the first register
    second_register = fetched_registers[1] # get the second register
    globals.registers[first_register] = globals.registers[second_register] 
    return PC+1

def subi(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find("$") # find the first occurrence $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    value = 0
    if fetched_registers[2].find("0x") != -1:
        value = int(fetched_registers[2],16)
    else:
        value = fetched_registers[2]
    temp_ans = int(globals.registers[fetched_registers[1]],16) - value
    hex_ans = ''
    if (temp_ans < 0):
        hex_ans = find_2s_complement(temp_ans)
    else:
        hex_ans = hex(temp_ans) #convert the integer back into hex form
     # store the hex back into registers and get rid of 0x in the beginning
    globals.registers[fetched_registers[0]] = hex_ans[2:]
    globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]].rjust(8,'0')
    if len(globals.registers[fetched_registers[0]]) > 8:
        globals.registers[fetched_registers[0]] = globals.registers[fetched_registers[0]][-8:]
    return PC+1

def beq(PC,code):
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    first_register = fetched_registers[0] # get the first register
    second_register = fetched_registers[1] # get the second register
    jump_target = fetched_registers[2] # the jump target
    if globals.registers[first_register] != globals.registers[second_register]: # if the contents are equal
       PC = PC+1
    else:
       PC = globals.label_dict[jump_target] # assign the PC
    return PC

def slt(PC,code):
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    if globals.registers[fetched_registers[1]] <  globals.registers[fetched_registers[2]]:
        globals.registers[fetched_registers[0]] = "00000001"
    else:
        globals.registers[fetched_registers[0]] = "00000000"
    return PC+1

def sb(PC,code):
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    word = globals.registers[fetched_registers[0]][-2:] # get the word to be stored
    jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
    address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
    dest_index = int(globals.registers[address_register],16) + jump - globals.base_address
    inner_index  = dest_index%4
    inner_index = 3-inner_index # because we follow little endian architecture
    inner_index = 2 * inner_index
    dest_index = dest_index // 4 # get the destination index
    globals.data_segment[dest_index][inner_index] = word[0]
    globals.data_segment[dest_index][inner_index+1] = word[1]
    return PC+1 # PC for next instruction

def lb(PC,code):
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    # get the word to be stored in the register
    jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
    address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
    dest_index = int(globals.registers[address_register],16) + jump - globals.base_address
    inner_index = dest_index%4
    inner_index = 3-inner_index # because we follow little endian architecture
    inner_index = 2 * inner_index
    dest_index = dest_index // 4 # get the destination index
    word = globals.data_segment[dest_index][inner_index:inner_index+2] # get the word from memory
    globals.registers[fetched_registers[0]] = "ffffffff"
    globals.registers[fetched_registers[0]][7] = word[0]
    globals.registers[fetched_registers[0]][8] = word[1]
    return PC+1

def syscall(PC):
    num = int(('0x'+globals.registers['$v0']), 16)
    stored = 0
    if num == 5: # Take integer input
        stored = int(input())
        if stored < 0:
            stored = find_2s_complement(stored)
        else:
            stored = hex(stored)
        globals.registers['$a0'] = stored[2:].rjust(8, '0')    
    elif num == 10: # Exit application
        print(globals.registers)
        print(globals.data_segment)
        print(hex(PC+base_pc).rjust(8,'0'))
        exit()
    elif num == 1:  # Output to console
        print(int(('0x'+globals.registers['$a0']), 16))
    return PC + 1
  # def jump_register(PC):
#     print(globals.registers)
#     print(globals.data_segment)
#     print(hex(PC+base_pc).rjust(8,'0'))
#     exit(0) # exit the program 
