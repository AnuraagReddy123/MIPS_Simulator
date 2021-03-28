from utility_func import find_2s_complement
import sim_glob

def ADD(a,b):
    return hex(int(a,16)+int(b,16))

def SUB(a,b):
    temp_ans = int(a,16) - int(b,16)
    hex_ans = ''
    if (temp_ans < 0):
        hex_ans = find_2s_complement(temp_ans)
    else:
        hex_ans = hex(temp_ans) #convert the integer back into hex form
    return temp_ans

def JUMP(PC,label):
    PC = sim_glob.label_dict[label]
    return PC

def BNE(a,b):
    if a != b:
        return 1
    else:
        return 0

def BEQ(a,b):
    if a == b:
        return 1:
    else:
        return 0