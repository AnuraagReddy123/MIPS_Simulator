
#program to simulate mips instructions
instructions = [] # list of the instructions read from the file
base_address = int("0x10010000",16) # address of the first byte
data_variables = {} # storing the index values
data_list = {} # storing the keys corresponding to the headers

registers = {'$r0' : '00000000','$at' : '00000000','$v0' : '00000000','$v1' : '00000000',
                  '$a0' : '00000000','$a1' : '00000000','$a2' : '00000000','$a3' : '00000000',
                  '$t0' : '10010000','$t1' : '00011223','$t2' : '00000000','$t3' : '00000000',
                  '$t4' : '00000000','$t5' : '00000000','$t6' : '00000000','$t7' : '00000000',
                  '$s0' : '00000000','$s1' : '00000000','$s2' : '00000000','$s3' : '00000000',
                  '$s4' : '00000000','$s5' : '00000000','$s6' : '00000000','$s7' : '00000000',
                  '$t8' : '00000000','$t9' : '00000000','$k0' : '00000000','$k1' : '00000000',
                  '$gp' : '00000000','$sp' : '00000000','$s8' : '00000000','$ra' : '00000000',}

data_segment = ['00000000'] * 10 #data segment (4 Kilobytes) , 10 bytes right now for testing

def SUB(PC,code):
    code = code.replace(" ","") #get rid of whitespaces
    index = code.find('$') #find first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually 
    # perform the subtraction operation on the registers and get the answer in decimal
    temp_ans = int(registers[fetched_registers[1]],16) - int(registers[fetched_registers[2]],16)
    hex_ans = hex(temp_ans) #convert the integer back into hex form
     # store the hex back into registers and get rid of 0x in the beginning
    registers[fetched_registers[0]] = hex_ans[2:]
    registers[fetched_registers[0]] = registers[fetched_registers[0]].rjust(8,'0')
    return PC+1

def BNE(PC,code):# for branch not equal instruction
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    first_register = fetched_registers[0] # get the first register
    second_register = fetched_registers[1] # get the second register
    jump_target = fetched_registers[2] # the jump target
    if registers[first_register] == registers[second_register]: # if the contents are equal
       PC = PC+1
    else:
       jump_to = instructions.index(jump_target) # find the target PC
       PC = jump_to # assign the PC
    return PC

def STORE(PC,code): # for store word instruction
    code = code.replace(" ","") # get rid of whitespaces
    index = code.find('$') # find the first occurrence of $
    reg_code = code[index:] # get the list of registers used
    fetched_registers = reg_code.split(",") # split the registers to access individually
    jump = int(fetched_registers[1][0:fetched_registers[1].find('(')])  # number of bytes to skip
    address_register = fetched_registers[1][fetched_registers[1].find('(')+1:fetched_registers[1].find(')')] # fetch the address register
    dest_index = int(registers[address_register],16) + jump - base_address
    remainder = dest_index  % 4 # the start byte within the word
    dest_index = dest_index // 4
    word = registers[fetched_registers[0]] # get the word to be stored
    skip = remainder * 2 # number of nibbles to skip
    # store the word in the data segment
    data_segment[dest_index] = data_segment[dest_index][0:skip] + word[0:(8-skip)]
    data_segment[dest_index+1] = word[8-skip:8] + data_segment[dest_index+1][skip:8]
    print(data_segment)
    return PC+4 # PC for next instruction

written = "sw $t1, 2($t0)" # test the instruction

PC = 0
PC = STORE(PC,written)
PC = STORE(PC,"sw $t1, 4($t0)")