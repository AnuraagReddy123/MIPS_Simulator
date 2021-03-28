import sim_glob


def find_2s_complement(num):
    num = bin(abs(num))[2:]
    n = len(num)
    
    i = n - 1
    while(i >= 0): 
        if (num[i] == '1'): 
            break
  
        i -= 1
  
    if (i == -1): 
        return '1'+num
  
    k = i - 1
    while(k >= 0): 
        if (num[k] == '1'): 
            num = list(num) 
            num[k] = '0'
            num = ''.join(num) 
        else: 
            num = list(num) 
            num[k] = '1'
            num = ''.join(num) 
  
        k -= 1
    return hex(int('0b'+num.rjust(32, '1'), 2))

def fetch_reg(instr):
    fetched_registers = []
    while instr.find("$") != -1:
        index = instr.find("$")
        fetched_registers.append(instr[index:index+3])
        instr = instr[index+3:]
    return fetched_registers


def fetch_imm(instr):
    instr = instr.replace(" ", "")
    index = instr.find("$")
    reg = instr[index:].split(",")
    index = reg[1].find("(")
    return reg[1][:index]


def op_type(instr):
    index = instr.find(" ")
    return instr[:index]

def clean_instruction(instr, instr_num):
    instr = instr.strip(' \t\n\r')
    instr = instr.replace("\n", "")

    # Searching for comments
    comment_index = instr.find('#')
    if comment_index != -1:
        globals.comments[instr[comment_index:]] = instr_num
        instr = instr.replace(instr[comment_index:], "")
        instr = instr.strip(' \t\n\r')

    return instr


if __name__ == "__main__":
    a = {}
    a['d'] = 10
    print(list(a.keys()))