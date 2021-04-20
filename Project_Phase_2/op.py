from utility_func import find_2s_complement
import sim_glob

def ADD(a,b):
    temp_ans = hex(int(a,16)+int(b,16))
    temp_ans = temp_ans[2:]
    temp_ans = temp_ans.rjust(8,'0')
    if len(temp_ans) > 8:
        temp_ans = temp_ans[-8:]
    return temp_ans

def SUB(a,b):
    temp_ans = int(a,16) - int(b,16)
    hex_ans = ''
    if (temp_ans < 0):
        hex_ans = find_2s_complement(temp_ans)
    else:
        hex_ans = hex(temp_ans) #convert the integer back into hex form
    hex_ans = hex_ans[2:]
    hex_ans = hex_ans.rjust(8,'0')
    if len(hex_ans) > 8:
        hex_ans = hex_ans[-8:]
    return hex_ans

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
        return 1
    else:
        return 0

def add_mem(a,b):
    temp = int(a,16) + int(b,16)
    return hex(temp)

def SLT(a, b):
    return hex(int(int(a, 16) < int(b, 16)))[2:].rjust(8,'0')