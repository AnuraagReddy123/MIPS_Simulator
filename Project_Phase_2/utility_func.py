import sim_glob

def fetch_reg(instr):
    instr = ""
    instr.replace(" ", "")
    index = instr.find("$")
    