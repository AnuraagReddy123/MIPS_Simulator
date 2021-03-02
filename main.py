from operations import add,jump,sub,bne,load,store

instructions = [] # list of the instructions read from the file
label_dict = {'loop' : '2'} # To store the indices of where the labels are occurring
data_dict = {'value' : 2} # storing the indices for data segment
comments = {}

base_address = int("0x10010000",16) # address of the first byte

registers = {'$r0' : '00000000','$at' : '00000000','$v0' : '00000000','$v1' : '00000000',
                  '$a0' : '00000000','$a1' : '00000000','$a2' : '00000000','$a3' : '00000000',
                  '$t0' : '10010000','$t1' : '00011223','$t2' : '00000000','$t3' : '00000000',
                  '$t4' : '00000000','$t5' : '00000000','$t6' : '00000000','$t7' : '00000000',
                  '$s0' : '00000000','$s1' : '00000000','$s2' : '00000000','$s3' : '00000000',
                  '$s4' : '00000000','$s5' : '00000000','$s6' : '00000000','$s7' : '00000000',
                  '$t8' : '00000000','$t9' : '00000000','$k0' : '00000000','$k1' : '00000000',
                  '$gp' : '00000000','$sp' : '00000000','$s8' : '00000000','$ra' : '00000000',}

data_segment = ['00000000'] * 1024 #data segment (4 Kilobytes)

def find_label (instr, instr_num):
    label_index = instr.find(":")
    if label_index != -1:
        label = instr[:label_index]
        label_dict[label] = instr_num
        instr = instr.replace(instr[:label_index+1], "")
    return instr

def clean_instruction(instr, instr_num):
    instr = instr.strip()
    instr = instr.replace("\n", "")
    
    #Searching for comments
    comment_index = instr.find('#')
    if comment_index != -1:
        comments[instr[comment_index:]] = instr_num
        instr = instr.replace(instr[comment_index:], "")
        instr = instr.strip()
    
    return instr


if __name__ == "__main__":
    instr_num = 0
    with open('instructions.txt', 'r') as file:
        for instr in file:
            instr = find_label(instr, instr_num)
            instr = clean_instruction(instr, instr_num)
            
            if (instr != ""):
                instructions.append(instr)
                instr_num += 1
        
        print(comments)
        print("\n")
        print(instructions)
        print("\n")
        print(label_dict)
        written = "sw $t1, value" # test the instruction