def initialize():
    global instructions
    global label_dict
    global data_dict
    global comments
    global base_address
    global registers
    global data_segment
    global fetched_instr
    global decoded_instr
    global result_of_execution
    global mem_result
    global queue
    global op_dict
    global latest_clock
    global stalled_instructions
    global data_forwarding
    global L1_cache
    global L2_cache
    global accessL1
    global accessL2
    L1_cache = ""
    L2_cache = ""
    accessL1 = 0
    accessL2 = 0
    latest_clock = 0
    instructions = []  # list of the instructions read from the file
    label_dict = {}  # To store the indices of where the labels are occurring
    data_dict = {}  # storing the indices for data segment
    comments = {}
    data_forwarding = True
    base_address = int("0x10010000", 16)  # address of the first byte

    registers = {'$ze': '00000000', '$at': '00000000', '$v0': '00000000', '$v1': '00000000',
                 '$a0': '00000000', '$a1': '00000000', '$a2': '00000000', '$a3': '00000000',
                 '$t0': '00000000', '$t1': '00000000', '$t2': '00000000', '$t3': '00000000',
                 '$t4': '00000000', '$t5': '00000000', '$t6': '00000000', '$t7': '00000000',
                 '$s0': '00000000', '$s1': '00000000', '$s2': '00000000', '$s3': '00000000',
                 '$s4': '00000000', '$s5': '00000000', '$s6': '00000000', '$s7': '00000000',
                 '$t8': '00000000', '$t9': '00000000', '$k0': '00000000', '$k1': '00000000',
                 '$gp': '00000000', '$sp': '00000000', '$s8': '00000000', '$ra': '00000000', }

    data_segment = ['00000000'] * 10  # data segment (4 Kilobytes)
    queue = []  # queue for storing stages of pipeline
    global que_reg
    que_reg = []  # list for keeping track of execution operations
    fetched_instr = ""
    # {"op": "load", src: "$r1", dest: "$r2", imm: "4"} or {"op": "add", src1: "r1", }
    decoded_instr = {}
    result_of_execution = {}
    mem_result = {}
    op_dict = {"ADD": 0, "SUB": 1, "BNE": 4, "BEQ": 5,
               "JUMP": 6, "LOAD": 2, "STORE": 3, "LI": 7, "SLT": 8}
    stalled_instructions = []
    '''
        OP CODES
        ADD     0
        SUB     1

        LOAD    2
        STORE   3

        BNE     4
        BEQ     5
        JUMP    6

        
    '''
    '''
    if() --> fetched_instr --> idrf() --> decoded_instr --> ex() --> result_of_execution --> (contd below)
                                                                 --> final_reg_value               
                                                                     (in case of add type instr)


    mem() --> mem_result -->            wb() --> final_reg_value
          --> final_reg_value
          (in case of load type instr)
    '''
