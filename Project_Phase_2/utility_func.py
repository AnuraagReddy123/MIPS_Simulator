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

def find_label(instr, instr_num):
    label_index = instr.find(":")
    if label_index != -1:
        label = instr[:label_index]
        sim_glob.label_dict[label] = instr_num
        instr = instr.replace(instr[:label_index+1], "")
    return instr

def store_data(data_num, data):
    for i in range(0, len(data)):
        #check whether value is hex or not
        hex_num = ""
        if data[i].find("0x")==-1:
            if int(data[i]) < 0:
                hex_num = find_2s_complement(int(data[i]))
            else:
                hex_num = hex(int(data[i]))
        else:
            hex_num = data[i]
        sim_glob.data_segment[i+data_num] = hex_num[2:]
        sim_glob.data_segment[i+data_num] = sim_glob.data_segment[i+data_num].rjust(8, '0')
    return data_num+len(data)

def edit_data(instr, data_num):
    instr = instr.replace(" ", "")
    variable_index = instr.find(":")
    if variable_index != -1:
        variable = instr[:variable_index]
        index = instr.find(".word")
        # Putting all the data in a list
        data = instr[index+5:].split(',')
        sim_glob.data_dict[variable] = data_num
        # Placing all data in data segment properly
        data_num = store_data(data_num, data)
    return data_num

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

def fetch_label(instr):
    instr = instr.replace(" ","")
    index = instr.find("$")
    reg = instr[index:].split(",")
    return reg[2]

def op_type(instr):
    index = instr.find(" ")
    return instr[:index]

def clean_instruction(instr, instr_num):
    instr = instr.strip(' \t\n\r')
    instr = instr.replace("\n", "")

    # Searching for comments
    comment_index = instr.find('#')
    if comment_index != -1:
        sim_glob.comments[instr[comment_index:]] = instr_num
        instr = instr.replace(instr[comment_index:], "")
        instr = instr.strip(' \t\n\r')

    return instr


if __name__ == "__main__":
    print(fetch_label("BEQ $R1, $R2, hey"))