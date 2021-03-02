import globals

def add(regs, s):
    reg1 = int(s.split()[2][2])
    reg2 = int(s.split()[3][2])
    reg_result = int(s.split()[1][2])
    regs[reg_result] = regs[reg1] + regs[reg2]

def jump(label_dict, label):
    pc = label_dict[label]
    return pc

def load(register, data, s):
    r = int(s.split()[1][2])
    mem = s.split()[2]
    register[r] = data[mem]

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
    return PC+1

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

# if __name__ == "__main__":
#     registers = [1, 2, 3, 0, 0, 0]                  # 6 Registers (r0, r1, r2, ... r6) Assume r3 register not for use Map
       
#     data = {"g": 5, "h": 4, "i": 3}                 #Store data in list

#     instructions = {"add $r0, $r0, $r1", "ld $r0, g"}
#     label_dict = {"main":0, "load": 1}

#     s = "add $r0, $r0, $r1"
#     if s.split()[0] == "add":
#         add(registers, s)
#     print(registers)

#     s = "jump load"

#     s = "ld $r0, g"
#     print(s.split())
#     load(registers, data, s)
#     print(registers)

#     s = "ld             $r0, g"
#     print(s.split())

#     while():
#         pc = jump()