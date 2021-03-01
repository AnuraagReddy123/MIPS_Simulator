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

if __name__ == "__main__":
    registers = [1, 2, 3, 0, 0, 0]                  # 6 Registers (r0, r1, r2, ... r6) Assume r3 register not for use Map
       
    data = {"g": 5, "h": 4, "i": 3}                 #Store data in list

    instructions = {"add $r0, $r0, $r1", "ld $r0, g"}
    label_dict = {"main":0, "load": 1}

    s = "add $r0, $r0, $r1"
    if s.split()[0] == "add":
        add(registers, s)
    print(registers)

    s = "jump load"

    s = "ld $r0, g"
    print(s.split())
    load(registers, data, s)
    print(registers)

    s = "ld             $r0, g"
    print(s.split())

    while():
        pc = jump()