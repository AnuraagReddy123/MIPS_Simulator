import sim_glob


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


if __name__ == "__main__":
    print(fetch_label("BEQ $R1, $R2, hey"))