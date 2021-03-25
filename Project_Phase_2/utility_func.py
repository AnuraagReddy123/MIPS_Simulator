import sim_glob

def fetch_reg(instr):
    fetched_registers = []
    instr.replace(" ", "")
    while instr.find("$") != -1:
        index = instr.find("$")
        fetched_registers.append(instr[index:index+3])
        instr = instr[index+3:]
    return fetched_registers